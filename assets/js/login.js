const DEMO_USER = { email: "admin@paraisotico.cr", password: "Paraiso2026" };
const DASHBOARD_URL = "dashboard/index.html";
const REMEMBER_KEY = "paraisoTicoEmail";
const SESSION_KEY = "paraisoTicoSession";
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MIN_PASSWORD_LENGTH = 8;
const REDIRECT_DELAY = 800;

const MESSAGES = {
   emailRequired: "Ingresa tu correo electrónico.",
   emailInvalid: "Ingresa un correo válido (ej.: nombre@correo.com).",
   passwordRequired: "Ingresa tu contraseña.",
   passwordShort: "La contraseña debe tener al menos " + MIN_PASSWORD_LENGTH + " caracteres.",
   wrongCredentials: "El correo o la contraseña no son correctos. Revisa los datos e inténtalo de nuevo.",
   loading: "Ingresando...",
};

const SELECTORS = {
   form: "#loginForm",
   email: "#loginEmail",
   password: "#loginPassword",
   remember: "#loginRemember",
   submit: "#loginSubmit",
   togglePassword: "#togglePassword",
   alert: "#loginAlert",
   toast: "#demoToast",
   unavailable: "[data-unavailable]",
};

$(function () {
   loadRememberedEmail();

   $(SELECTORS.email).on("blur", () => validateField({ input: $(SELECTORS.email), getError: getEmailError }));
   $(SELECTORS.password).on("blur", () => validateField({ input: $(SELECTORS.password), getError: getPasswordError }));
   $(SELECTORS.email + ", " + SELECTORS.password).on("input", onFieldInput);
   $(SELECTORS.togglePassword).on("click", onTogglePassword);
   $(SELECTORS.unavailable).on("click", onUnavailableFeature);
   $(SELECTORS.form).on("submit", onSubmitLogin);
});

const getEmailError = (value) => {
   const email = value.trim();

   if (!email) {
      return MESSAGES.emailRequired;
   }

   if (!EMAIL_PATTERN.test(email)) {
      return MESSAGES.emailInvalid;
   }

   return "";
};

const getPasswordError = (value) => {
   if (!value) {
      return MESSAGES.passwordRequired;
   }

   if (value.length < MIN_PASSWORD_LENGTH) {
      return MESSAGES.passwordShort;
   }

   return "";
};

const validateField = ({ input, getError }) => {
   const field = input.closest(".loginField");
   const errorMessage = getError(input.val());
   const isValid = errorMessage === "";

   field.toggleClass("isValid", isValid).toggleClass("isInvalid", !isValid);
   field.find(".fieldStatus").text(isValid ? "check_circle" : "error");
   field.find(".fieldError").text(errorMessage);
   input.attr("aria-invalid", !isValid);

   return isValid;
};

const onFieldInput = function () {
   const input = $(this);
   const isEmail = input.is(SELECTORS.email);

   hideAlert();

   if (input.closest(".loginField").hasClass("isInvalid")) {
      validateField({ input, getError: isEmail ? getEmailError : getPasswordError });
   }
};

const onTogglePassword = () => {
   const passwordInput = $(SELECTORS.password);
   const toggleButton = $(SELECTORS.togglePassword);
   const isHidden = passwordInput.attr("type") === "password";

   passwordInput.attr("type", isHidden ? "text" : "password");
   toggleButton.attr("aria-pressed", isHidden).attr("aria-label", isHidden ? "Ocultar contraseña" : "Mostrar contraseña");
   toggleButton.find(".material-symbols-rounded").text(isHidden ? "visibility_off" : "visibility");
};

const onUnavailableFeature = (event) => {
   event.preventDefault();
   bootstrap.Toast.getOrCreateInstance($(SELECTORS.toast)[0]).show();
};

const onSubmitLogin = (event) => {
   event.preventDefault();
   hideAlert();

   const emailInput = $(SELECTORS.email);
   const passwordInput = $(SELECTORS.password);
   const isEmailValid = validateField({ input: emailInput, getError: getEmailError });
   const isPasswordValid = validateField({ input: passwordInput, getError: getPasswordError });

   if (!isEmailValid || !isPasswordValid) {
      (isEmailValid ? passwordInput : emailInput).trigger("focus");
      return;
   }

   const email = emailInput.val().trim().toLowerCase();
   const password = passwordInput.val();

   if (!isDemoUser({ email, password })) {
      showAlert(MESSAGES.wrongCredentials);
      passwordInput.val("").trigger("focus");
      $(SELECTORS.password).closest(".loginField").removeClass("isValid");
      return;
   }

   saveRememberedEmail({ email, shouldRemember: $(SELECTORS.remember).is(":checked") });
   writeStorage({ storage: window.sessionStorage, key: SESSION_KEY, value: email });
   setLoadingState(true);

   setTimeout(() => {
      window.location.href = DASHBOARD_URL;
   }, REDIRECT_DELAY);
};

const isDemoUser = ({ email, password }) => {
   return email === DEMO_USER.email && password === DEMO_USER.password;
};

const showAlert = (message) => {
   const alert = $(SELECTORS.alert);

   alert.find(".loginAlertText").text(message);
   alert.removeClass("d-none");
};

const hideAlert = () => {
   $(SELECTORS.alert).addClass("d-none");
};

const setLoadingState = (isLoading) => {
   const submitButton = $(SELECTORS.submit);

   submitButton.prop("disabled", isLoading);
   submitButton.find(".submitText").text(isLoading ? MESSAGES.loading : "Iniciar sesión");
   submitButton.find(".submitIcon").toggleClass("d-none", isLoading);
   submitButton.find(".spinner-border").remove();

   if (isLoading) {
      submitButton.prepend('<span class="spinner-border spinner-border-sm" aria-hidden="true"></span>');
   }
};

const loadRememberedEmail = () => {
   const rememberedEmail = readStorage({ storage: window.localStorage, key: REMEMBER_KEY });

   if (!rememberedEmail) {
      return;
   }

   $(SELECTORS.email).val(rememberedEmail);
   $(SELECTORS.remember).prop("checked", true);
};

const saveRememberedEmail = ({ email, shouldRemember }) => {
   writeStorage({ storage: window.localStorage, key: REMEMBER_KEY, value: shouldRemember ? email : null });
};

const readStorage = ({ storage, key }) => {
   try {
      return storage.getItem(key);
   } catch (error) {
      return null;
   }
};

const writeStorage = ({ storage, key, value }) => {
   try {
      if (value === null) {
         storage.removeItem(key);
         return;
      }

      storage.setItem(key, value);
   } catch (error) {
      return;
   }
};
