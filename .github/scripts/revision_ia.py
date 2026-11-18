import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request
from datetime import datetime

COMMENT_MARKER = "<!-- revision-ia -->"
CODE_EXTENSIONS = (".html", ".htm", ".css", ".js", ".php", ".py")
IGNORED_PATHS = ("assets/vendor/", ".min.", "data/", "docs/", ".github/")
HIGH_THRESHOLD = int(os.environ.get("UMBRAL_ALTO", "60"))
AMBIGUOUS_THRESHOLD = int(os.environ.get("UMBRAL_AMBIGUO", "30"))
SHOULD_FAIL_ON_HIGH = os.environ.get("FALLAR_SI_ALTO", "false").lower() == "true"
AI_TRAILER_FLOOR = 90

LEFTOVER_PATTERNS = [r"```", r"\bhere'?s\b", r"\bhere is the\b", r"\bcertainly\b", r"\bas an ai\b", r"\blanguage model\b", r"aqu[ií] tienes", r"aqu[ií] est[aá] el c[oó]digo", r"¡claro", r"\bclaro, ", r"\bchatgpt\b", r"\bopenai\b", r"\bcopilot\b", r"\bclaude\b", r"\bgemini\b", r"\bgenerated (by|with)\b", r"\bgenerado (por|con)\b", r"\byour[_ ]api[_ ]key\b", r"\breplace with your\b", r"\blet me\b", r"\bi'?ve\b"]
TUTORIAL_PATTERNS = [r"esta funci[oó]n", r"este c[oó]digo", r"esta secci[oó]n", r"funci[oó]n (para|que)", r"se encarga de", r"aqu[ií] se", r"a continuaci[oó]n", r"ejemplo de uso", r"\bnota:", r"\bimportante:", r"\bpaso \d", r"\basegura", r"\bopcional:", r"\bpuedes\b", r"\breemplaza", r"this function", r"this code", r"\bhelper\b", r"\bhandles?\b", r"\bensures?\b", r"make sure", r"\bnote:", r"\bexample\b", r"\bstep \d", r"\bhere we\b", r"\bnow we\b", r"\binitiali[sz]e", r"\bcheck if\b", r"\b(get|set|update|add) the\b", r"\byou can\b"]
ENGLISH_WORDS_PATTERN = r"\b(the|and|this|with|for|if|when|to|of|is)\b"
EMOJI_PATTERN = "[\U0001F300-\U0001FAFF☀-➿⭐✅]"
BANNER_PATTERN = r"(={4,}|-{4,}|\*{4,}|#{4,})"
JSDOC_PATTERN = r"@(param|returns?|type|typedef|example|description)\b"

MODERN_PATTERNS = {
    ".js": [r"\basync\b", r"\bawait\b", r"\bfetch\(", r"\?\.", r"\?\?", r"`[^`]*\$\{", r"\bclass\s+\w+", r"^\s*(import|export)\b", r"\bnew\s+(IntersectionObserver|MutationObserver|ResizeObserver|AbortController|Promise|Map|Set)\b", r"\.(then|finally)\(", r"\bObject\.(entries|fromEntries|freeze)\b", r"\.(reduce|flatMap)\("],
    ".css": [r"\bclamp\(", r":(has|is|where)\(", r"\binset\s*:", r"\baspect-ratio\b", r"(rgb|hsl)a?\([^)]*/", r"\bcolor-mix\(", r"@(layer|container|supports)\b", r"\b(min|max)\(", r"\b[dsl]vh\b", r"prefers-(reduced-motion|color-scheme)", r"\bbackdrop-filter\b", r":focus-visible", r"text-wrap\s*:\s*balance", r"mix-blend-mode"],
    ".php": [r"declare\(strict_types", r"\)\s*:\s*\??(string|int|bool|array|void|float|never|mixed)\b", r"\bmatch\s*\(", r"\?->", r"\bfn\s*\(", r"\breadonly\b", r"\benum\s+\w+", r"str_(contains|starts_with|ends_with)\("],
    ".py": [r"\basync\b", r"\bawait\b", r"->\s*\w+", r":\s*(str|int|bool|list|dict)\b\s*[=,)]", r"\bdataclass\b", r"\bmatch\s+\w+:"],
}
POLISH_PATTERNS = [r"\baria-[a-z]+=", r"\brole=\"", r"rel=\"noopener", r"loading=\"lazy\"", r"decoding=\"async\"", r"autocomplete=\"", r"<picture\b", r"srcset=", r"novalidate", r"<(header|nav|main|section|article|aside|footer)\b"]
DEFENSIVE_PATTERNS = [r"\btry\s*\{", r"\btry:", r"\bcatch\s*\(", r"\bexcept\b", r"console\.(error|warn)\(", r"typeof\s+\w+\s*===", r"\bthrow new\b", r"\braise\b"]
AI_TRAILER_PATTERN = r"(co-authored-by:.*(claude|copilot|chatgpt|openai|cursor|gemini|anthropic|noreply@anthropic)|generated with|generado con|🤖)"

SIGNAL_LABELS = {
    "leftovers": "texto típico de una respuesta de IA",
    "tutorial": "comentarios con tono de tutorial",
    "english": "comentarios en inglés",
    "commentRatio": "muchos comentarios",
    "emoji": "emojis en comentarios",
    "banners": "separadores decorativos",
    "jsdoc": "bloques JSDoc",
    "modern": "sintaxis avanzada para el curso",
    "polish": "accesibilidad/semántica muy completa",
    "defensive": "manejo de errores defensivo",
    "bulk": "archivo grande agregado de una vez",
}


def run_git(args):
    return subprocess.run(["git"] + args, capture_output=True, text=True, check=True).stdout


def is_code_file(path):
    return path.lower().endswith(CODE_EXTENSIONS) and not any(ignored in path for ignored in IGNORED_PATHS)


def get_extension(path):
    extension = os.path.splitext(path)[1].lower()
    return ".html" if extension == ".htm" else extension


def get_changed_files(base, head):
    files = []

    for line in run_git(["diff", "--numstat", "--diff-filter=AM", base + "..." + head]).splitlines():
        added, _, path = line.split("\t", 2)

        if added == "-" or not is_code_file(path):
            continue

        is_new = run_git(["diff", "--name-only", "--diff-filter=A", base + "..." + head, "--", path]).strip() != ""
        files.append({"path": path, "isNew": is_new})

    return files


def get_added_lines(base, head, path):
    diff = run_git(["diff", "-U0", base + "..." + head, "--", path])
    return [line[1:] for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++") and line[1:].strip()]


def get_comments(lines, extension):
    comments = []
    is_inside_block = False

    for line in lines:
        text = line.strip()

        if is_inside_block or text.startswith(("/*", "<!--")):
            comments.append(text)
            is_inside_block = not ("*/" in text or "-->" in text)
            continue

        if text.startswith("*") and extension in (".js", ".css", ".php"):
            comments.append(text)
            continue

        if extension in (".js", ".php") and "//" in text and not re.search(r"https?://", text):
            comments.append(text[text.index("//"):])
            continue

        if extension in (".py", ".php") and text.startswith("#"):
            comments.append(text)

    return comments


def count_matches(patterns, text):
    return sum(len(re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)) for pattern in patterns)


def get_density(count, total):
    return count * 100 / max(total, 1)


def score_file(base, head, file):
    path = file["path"]
    extension = get_extension(path)
    lines = get_added_lines(base, head, path)
    total = len(lines)

    if total == 0:
        return None

    code = "\n".join(lines)
    comments = get_comments(lines, extension)
    comment_text = "\n".join(comments).lower()
    comment_ratio = len(comments) / total

    signals = {
        "leftovers": min(50, count_matches(LEFTOVER_PATTERNS, code) * 25),
        "tutorial": min(30, count_matches(TUTORIAL_PATTERNS, comment_text) * 6),
        "english": min(15, sum(3 for comment in comments if len(re.findall(ENGLISH_WORDS_PATTERN, comment, re.IGNORECASE)) >= 2)),
        "commentRatio": round(min(15, max(0, (comment_ratio - 0.1) / 0.3 * 15))),
        "emoji": min(20, len(re.findall(EMOJI_PATTERN, comment_text)) * 10),
        "banners": min(15, len(re.findall(BANNER_PATTERN, comment_text)) * 5),
        "jsdoc": min(20, len(re.findall(JSDOC_PATTERN, comment_text)) * 5),
        "modern": round(min(30, get_density(count_matches(MODERN_PATTERNS.get(extension, []), code), total) * 3)),
        "polish": round(min(20, get_density(count_matches(POLISH_PATTERNS, code), total) * 1.5)) if extension == ".html" else 0,
        "defensive": min(15, count_matches(DEFENSIVE_PATTERNS, code) * 4) if extension in (".js", ".php", ".py") else 0,
        "bulk": (15 if total > 300 else 10 if total > 150 else 0) if file["isNew"] else 0,
    }

    return {"path": path, "lines": total, "score": min(100, sum(signals.values())), "signals": signals}


def get_commits(base, head):
    output = run_git(["log", "--no-merges", "--reverse", "--format=%x1e%H%x1f%an%x1f%aI%x1f%s%x1f%B%x1f", "--numstat", base + ".." + head])
    commits = []

    for record in output.split("\x1e")[1:]:
        sha, author, date, subject, body, stats = record.split("\x1f", 5)
        code_lines = 0

        for line in stats.strip().splitlines():
            parts = line.split("\t", 2)

            if len(parts) == 3 and parts[0] != "-" and is_code_file(parts[2]):
                code_lines += int(parts[0])

        commits.append({"sha": sha[:7], "author": author, "date": datetime.fromisoformat(date), "subject": subject, "body": body, "lines": code_lines})

    return commits


def score_commits(commits):
    bonus = 0
    has_ai_trailer = False
    previous_date = None

    for commit in commits:
        notes = []

        if re.search(AI_TRAILER_PATTERN, commit["body"], re.IGNORECASE):
            has_ai_trailer = True
            notes.append("el mensaje menciona una herramienta de IA")

        if commit["lines"] >= 400:
            bonus += 10
            notes.append(str(commit["lines"]) + " líneas de código en un solo commit")

        if previous_date and commit["lines"] >= 150:
            minutes = (commit["date"] - previous_date).total_seconds() / 60

            if minutes <= 1:
                bonus += 10
                notes.append("creado en el mismo minuto que el commit anterior")
            elif minutes <= 30 and commit["lines"] / minutes >= 20:
                bonus += 15
                notes.append(str(round(commit["lines"] / minutes)) + " líneas por minuto desde el commit anterior")

        commit["notes"] = notes
        previous_date = commit["date"]

    return {"bonus": min(25, bonus), "hasAiTrailer": has_ai_trailer}


def get_level(score):
    if score >= HIGH_THRESHOLD:
        return "🔴 Alto"

    if score >= AMBIGUOUS_THRESHOLD:
        return "🟡 Ambiguo"

    return "🟢 Bajo"


def get_top_signals(signals):
    active = sorted([(points, name) for name, points in signals.items() if points > 0], reverse=True)
    return ", ".join(SIGNAL_LABELS[name] + " (+" + str(points) + ")" for points, name in active[:3]) or "—"


def build_report(files, commits, commit_result):
    total_lines = sum(file["lines"] for file in files)
    files_score = sum(file["score"] * file["lines"] for file in files) / total_lines if total_lines else 0
    score = min(100, round(files_score + commit_result["bonus"]))

    if commit_result["hasAiTrailer"]:
        score = max(score, AI_TRAILER_FLOOR)

    report = [COMMENT_MARKER, "## 🤖 Revisión de posible código generado con IA", ""]
    report.append("**Índice del PR: " + str(score) + " % — " + get_level(score) + "**")
    report.append("")
    report.append("Escala: 🟢 menos de " + str(AMBIGUOUS_THRESHOLD) + " % · 🟡 " + str(AMBIGUOUS_THRESHOLD) + "–" + str(HIGH_THRESHOLD - 1) + " % · 🔴 " + str(HIGH_THRESHOLD) + " % o más")
    report.append("")
    report.append("> El índice se calcula con señales del código y de los commits; no es una prueba. Con un índice alto, revisa los archivos marcados y pídele al autor que explique ese código antes de aprobar.")
    report.append("")

    if not files:
        report.append("Este PR no agrega código HTML, CSS, JS, PHP ni Python para analizar.")
        return score, "\n".join(report)

    report.append("### Archivos")
    report.append("")
    report.append("| Archivo | Líneas añadidas | Índice | Nivel | Señales principales |")
    report.append("|---|---|---|---|---|")

    for file in sorted(files, key=lambda item: item["score"], reverse=True):
        report.append("| `" + file["path"] + "` | " + str(file["lines"]) + " | " + str(file["score"]) + " % | " + get_level(file["score"]) + " | " + get_top_signals(file["signals"]) + " |")

    report.append("")
    report.append("### Commits")
    report.append("")
    report.append("| Commit | Autor | Líneas de código | Observaciones |")
    report.append("|---|---|---|---|")

    for commit in commits:
        report.append("| `" + commit["sha"] + "` " + commit["subject"].replace("|", "\\|") + " | " + commit["author"] + " | " + str(commit["lines"]) + " | " + ("; ".join(commit["notes"]) or "—") + " |")

    report.append("")
    report.append("<details><summary>Cómo se calcula</summary>")
    report.append("")
    report.append("Cada archivo suma puntos por señales en las líneas añadidas: texto típico de respuestas de IA, comentarios con tono de tutorial o en inglés, exceso de comentarios, emojis, JSDoc, separadores decorativos, sintaxis avanzada para el nivel del curso, accesibilidad muy completa, manejo de errores defensivo y archivos grandes agregados de una vez. El índice del PR es el promedio ponderado por líneas, más puntos por commits muy grandes o hechos demasiado rápido. Si un commit menciona una herramienta de IA (por ejemplo, un `Co-Authored-By`), el índice sube al menos a " + str(AI_TRAILER_FLOOR) + " %.")
    report.append("")
    report.append("</details>")

    return score, "\n".join(report)


def call_github(method, url, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", "Bearer " + token)
    request.add_header("Accept", "application/vnd.github+json")

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode() or "null")


def publish_comment(report):
    token = os.environ["GITHUB_TOKEN"]
    comments_url = "https://api.github.com/repos/" + os.environ["GITHUB_REPOSITORY"] + "/issues/" + os.environ["PR_NUMBER"] + "/comments"
    existing = [comment for comment in call_github("GET", comments_url + "?per_page=100", token) if COMMENT_MARKER in (comment.get("body") or "")]

    if existing:
        call_github("PATCH", existing[0]["url"], token, {"body": report})
        return

    call_github("POST", comments_url, token, {"body": report})


def write_summary(report):
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")

    if not summary_path:
        return

    with open(summary_path, "a", encoding="utf-8") as summary:
        summary.write(report + "\n")


def main():
    parser = argparse.ArgumentParser(description="Calcula un índice de posible código generado con IA para un PR.")
    parser.add_argument("--base", default=os.environ.get("BASE_SHA"))
    parser.add_argument("--head", default=os.environ.get("HEAD_SHA", "HEAD"))
    parser.add_argument("--publicar", action="store_true", default=bool(os.environ.get("PR_NUMBER")))
    options = parser.parse_args()

    if not options.base:
        sys.exit("Falta la rama base: usa --base origin/main o define BASE_SHA.")

    files = [result for result in (score_file(options.base, options.head, file) for file in get_changed_files(options.base, options.head)) if result]
    commits = get_commits(options.base, options.head)
    score, report = build_report(files, commits, score_commits(commits))

    print(report)
    write_summary(report)

    if options.publicar:
        publish_comment(report)

    if score >= HIGH_THRESHOLD:
        print("::warning title=Posible código con IA::El índice del PR es " + str(score) + " %. Revisa el comentario del PR antes de aprobar.")

        if SHOULD_FAIL_ON_HIGH:
            sys.exit(1)


if __name__ == "__main__":
    main()
