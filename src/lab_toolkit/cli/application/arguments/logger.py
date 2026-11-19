def add_display_arguments(parser):
    """Ajoute les options de sélection du mode d'affichage."""

    display_group = parser.add_mutually_exclusive_group()

    display_group.add_argument(
        "--display-simple",
        dest="display_mode",
        action="store_const",
        const="simple",
        help="Affichage synthétique.",
    )

    display_group.add_argument(
        "--display-pipeline",
        dest="display_mode",
        action="store_const",
        const="pipeline",
        help="Affichage chronologique des appels.",
    )

    display_group.add_argument(
        "--display-tree",
        dest="display_mode",
        action="store_const",
        const="tree",
        help="Affichage hiérarchique des appels.",
    )

    parser.set_defaults(display_mode="pipeline")
