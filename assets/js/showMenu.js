const onToggleMenu = () => {
   $(".mobile-menu").toggleClass("is-open");
};

$(document).on("click", ".menu-icon-container", onToggleMenu);
