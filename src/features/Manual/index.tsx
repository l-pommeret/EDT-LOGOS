import React, { Suspense } from "react";
import { useParams } from "react-router-dom";
import { Group } from "../../groups";
import { routeParams } from "../routing";

const Calendar = React.lazy(() => import("../Calendar"));

interface ManualProps {
  allGroups: Group[];
}

/**
 * Renders a manual selection of groups and displays a calendar with the selected groups.
 */
export default function Manual({ allGroups }: ManualProps) {
  const { selectedGroups } = useParams<typeof routeParams.selectedGroups>();

  if (!selectedGroups) {
    return null;
  }

  const listOfGroups = selectedGroups.split("+");

  return (
    <Suspense fallback={<div>Chargement du calendrier...</div>}>
      <h1>Choix manuel</h1>
      <Calendar
        groups={allGroups.filter((g) => listOfGroups.includes(g.id))}
      />
    </Suspense>
  );
}
