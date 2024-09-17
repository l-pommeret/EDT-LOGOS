import React from "react";
import { NavLink, NavLinkProps } from "react-router-dom";

import * as styles from "./Layout.module.css";
import logo from "./upc.svg";
import Icon from "../Icon";

/**
 * The Navbar component displays the navigation bar of the application.
 */
export function Navbar() {
  const maybeActiveClassName: NavLinkProps["className"] =
    ({ isActive }) => isActive ? styles["active"] : undefined;

  return (
    <nav className={styles["navbar"]}>

      {/* Logo */}
      <a
        href="https://u-paris.fr"
        title="Université de Paris"
      >
        <img src={logo} alt="Logo de l'Université de Paris" />
      </a>
      <NavLink
        to="/parcours"
        className={maybeActiveClassName}
      >
        <Icon name="calendar-alt" space />
        Accueil
      </NavLink>
      <a href="review/archive23-24/#">Archives</a>
      <NavLink
        to="/aide"
        className={maybeActiveClassName}
      >
        <Icon name="question" space />
        À Propos
      </NavLink>
    </nav>
  );
}
