# https://django-jazzmin.readthedocs.io/

JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "JSC Order Tracker",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "JSC Order Tracker",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "JSC Order Tracker",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "assets/img/c_truck.png",
    # CSS classes that are applied to the logo above
    "site_logo_classes": None,
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": "assets/img/c_truck.png",
    # Welcome text on the login screen
    "welcome_sign": "Welcome to JSC Order Tracker",
    # Copyright on the footer
    "copyright": "",
    # The model admin to search from the search bar, search bar omitted if excluded
    # "search_model": "auth.User",
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index"},
        # external url that opens in a new window (Permissions can be added)
        # {"name": "Support", "url": "https://github.com/farridav/django-jazzmin/issues", "new_window": True},
        # model admin to link to (Permissions checked against model)
        # {"model": "accounts.CustomUser"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "schedules"},
        {"app": "orders"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {"name": "Support", "url": "https://www.techvo.net/support-center#gform_4", "new_window": True},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": False,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [
        "core",
    ],
    # Hide these models when generating side menu (e.g auth.user)
    # "hide_models": ["supplies.GravelItem", "concrete.ConcreteType"],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": [
        "concrete",
        "gravel",
        "schedules",
        "orders",
        "sites",
        "clients",
        "supplies",
        "accounts",
    ],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        # "accounts": [
        #     {
        #         "name": "Notes",
        #         "url": "/core/notemodel/",
        #         "icon": "fas fa-comment",
        #     }
        # ],
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "accounts": "fas fa-users-cog",
        "accounts.CustomUser": "fas fa-user",
        "accounts.Group": "fas fa-users",
        "clients": "fas fa-building",
        "clients.Client": "fas fa-building",
        "clients.Site": "fas fa-layer-group",
        "supplies": "fas fa-store-alt",
        "supplies.GravelItem": "fas fa-bezier-curve",
        "supplies.Supplier": "fas fa-store-alt",
        "orders": "fas fa-receipt",
        "orders.ConcreteOrder": "fa fa-window-minimize",
        "orders.GravelOrder": "fa fa-cubes",
        "orders.PumpOrder": "fa fa-faucet",
        "schedules": "fas fa-calendar",
        "schedules.GravelDeliverySchedule": "fa fa-cubes",
        "schedules.ConcreteOrderSchedule": "fa fa-window-minimize",
        "schedules.PumpOrder": "fa fa-faucet",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": True,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    # "changeform_format_overrides": {"apps.accounts.CustomUser": "collapsible", "accounts.group": "vertical_tabs"},
    # Add a language dropdown into the admin
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": True,
    "footer_small_text": True,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-secondary",
    "accent": "accent-info",
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-navy",
    "sidebar_nav_small_text": True,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "lumen",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
    "actions_sticky_top": True,
}
