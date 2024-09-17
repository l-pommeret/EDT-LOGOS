import React, { Suspense } from "react";
import { useParams } from "react-router-dom";
import { Group } from "../../groups";
import { getParcoursIconName, getParcoursTitle } from "../../config";
import { routeParams } from "../routing";
import Icon from "../Icon";

const Calendar = React.lazy(() => import("../Calendar"));

/**
 * Filter `calendars.json`.
 * @param allGroups The list of all groups currently considered.
 * @param parcours The parcours of the groups to return.
 * @param year The year of the groups to return.
 * @returns A list of groups matching both parameters.
 */
export function filterCalendars(allGroups: Group[], parcours: string, year: string): Group[] {
  return allGroups.filter(
    (cal) => cal.parcours === parcours && cal.year === year,
  );
}

interface CalendarWrappersProps {
  allGroups: Group[];
}

/**
 * Affiche un calendrier correspondant à une combinaison parcours + année.
 * Sur les URL du type /parcours/...
 * En cas d'URL du type /parcours/.../.../..., on affiche un groupe pré-selectionné par défaut.
 */
export default function CalendarWrapper({ allGroups }: CalendarWrappersProps) {
  const { parcours } = useParams<typeof routeParams.parcours>();
  const { year } = useParams<typeof routeParams.year>();
  const { selectedGroups } = useParams<typeof routeParams.selectedGroups>();

  if (!year || !parcours) {
    return null;
  }

  const iconName = getParcoursIconName(parcours);

  return (
    <>
      <h2>
        Calendrier choisi&nbsp;:
        {" "}
        {iconName && <Icon name={iconName} space />}
        {getParcoursTitle(parcours)}
        {" "}
        &ndash;
        {" "}
        {year.toUpperCase()}
      </h2>

      <Suspense fallback={<div>Chargement du calendrier...</div>}>
        <Calendar
          key={parcours}
          selectedGroups={selectedGroups}
          groups={filterCalendars(allGroups, parcours, year)}
        />
      </Suspense>
    </>
  );
}
