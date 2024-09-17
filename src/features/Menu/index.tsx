import React, { useEffect, useState } from "react";
import { Navigate, useLocation, useParams } from "react-router";
import { Outlet } from "react-router-dom";

import { Group } from "../../groups";
import ParcoursMenu from "./ParcoursMenu";
import YearMenu from "./YearMenu";

import * as styles from "./Menu.module.css";
import { routeParams } from "../routing";

interface MenuProps {
  /** List of all available groups. */
  allGroups: Group[];
}

export interface ChildMenuProps extends MenuProps {
  /** Whether the menu is expanded or not. */
  expanded: boolean;
}

/**
 * The Menu component displays a list of available calendars and allows the user to navigate to them.
 * It consists of a ParcoursMenu and a YearMenu, which display the available calendars grouped by parcours and year, respectively.
 * The component also includes a button to toggle the visibility of the menus.
 */
export default function Menu({ allGroups }: MenuProps) {
  const { year } = useParams<typeof routeParams.year>();
  const { pathname } = useLocation();
  const [expanded, setExpanded] = useState(false);

  useEffect(() => {
    // if a year is shown, set expanded to false, otherwise, set it to true
    // I know I could write setExpanded(!!year). But this is more explicit.
    if (year) {
      setExpanded(false);
    } else {
      setExpanded(true);
    }
  }, [year]);

  if (year === "year") {
    console.warn("Old URL detected, redirecting to new URL.");
    return <Navigate to={pathname.replace("/year", "")} replace />;
  }

  return (
    <>
      <h1>Emplois du temps</h1>

      <button
        type="button"
        onClick={() => setExpanded(v => !v)}
        className={styles["expander"]}
      >
        <div>Menu</div>
        <div>{expanded ? "▼" : "▶"}</div>
      </button>

      <ParcoursMenu expanded={expanded} allGroups={allGroups} />
      <YearMenu expanded={expanded} allGroups={allGroups} />

      <Outlet />
    </>
  );
}
