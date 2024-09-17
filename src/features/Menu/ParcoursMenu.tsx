import React, { useMemo } from "react";
import { NavLink } from "react-router-dom";
import { ChildMenuProps } from ".";
import { getParcoursIconName, getParcoursTitle } from "../../config";

import * as styles from "./Menu.module.css";
import Icon from "../Icon";

export default function ParcoursMenu({ expanded, allGroups }: ChildMenuProps) {
  const parcours = useMemo(() =>
    Array.from(new Set(allGroups.map(g => g.parcours))).sort(),
    [allGroups]);

  return (
    <div className={styles["menu"] + (expanded ? ` ${styles["expanded"]}` : "")}>
      <h2>Choissisez une filière&nbsp;:</h2>

      <nav>
        {parcours.map((parcours) => {
          const iconName = getParcoursIconName(parcours);
          const icon = iconName ? <Icon name={iconName} space /> : null;

          return (
            <NavLink
              key={parcours}
              to={`/parcours/${parcours}`}
              className={({ isActive }) => isActive ? styles["active"] : undefined}
              title={`Aller à la page du parcours ${getParcoursTitle(parcours)} [${parcours}]`}
            >
              {icon}
              {getParcoursTitle(parcours)}
            </NavLink>
          );
        })}
      </nav>
    </div>
  );
}
