import React, { useMemo } from "react";
import { NavLink, useParams } from "react-router-dom";
import { ChildMenuProps } from ".";

import * as styles from "./Menu.module.css";
import { routeParams } from "../routing";

/**
 * Un composant qui donne le choix entre les différentes années (L1, L2...) d'un parcours.
 * Redirige sur l'URL /parcours/.../year/...
 */
export default function YearMenu({ expanded, allGroups }: ChildMenuProps) {
  const { parcours } = useParams<typeof routeParams.parcours>();

  const years = useMemo(() =>
    Array.from(new Set(allGroups.filter(g => g.parcours === parcours).map(g => g.year))).sort(),
    [allGroups, parcours]);

  if (!parcours) {
    return null;
  }

  return (
    <div className={styles["menu"] + (expanded ? ` ${styles["expanded"]}` : "")}>
      <h2>Choisissez une année&nbsp;:</h2>

      <nav>
        {years.map(y => (
          <NavLink
            key={y}
            to={`/parcours/${parcours}/${y}`}
            className={({ isActive }) => isActive ? styles["active"] : undefined}
            title={`Aller à la page de l'année ${y.toUpperCase()}`}
          >
            {y.toUpperCase()}
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
