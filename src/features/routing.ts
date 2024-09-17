/**
 * @description Routes of the application.
 */
export const routes = {
    /** The page with the help. */
    aide: "aide",
    /** The page with the manual choice of groups. */
    manuel: "manuel",
    /** The parcours page. */
    parcours: "parcours",
} as const;

/**
 * @description URL parameters of the application.
 */
export const routeParams = {
    parcours: "parcours",
    selectedGroups: "selectedGroups",
    year: "year",
} as const;
