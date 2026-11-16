const COMPONENT_SELECTOR = "[data-component]";
const DEFAULT_PAGE = "index.html";
const CURRENT_PAGE_LINKS = ".nav-link, .bookButton";

$(function () {
   const currentPage = getCurrentPage();

   $(COMPONENT_SELECTOR).each(function () {
      loadComponent({ container: $(this), currentPage });
   });
});

const getCurrentPage = () => {
   return window.location.pathname.split("/").pop() || DEFAULT_PAGE;
};

const loadComponent = ({ container, currentPage }) => {
   const componentPath = container.data("component");

   container.load(componentPath, (response, status) => {
      if (status === "error") {
         console.error("No se pudo cargar el componente: " + componentPath);
         return;
      }

      markCurrentPage({ container, currentPage });
   });
};

const markCurrentPage = ({ container, currentPage }) => {
   const currentLinks = container.find(CURRENT_PAGE_LINKS).filter('[href="' + currentPage + '"]');

   currentLinks.attr("aria-current", "page");
   currentLinks.filter(".nav-link").addClass("active");
};
