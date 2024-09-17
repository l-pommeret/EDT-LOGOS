import { IconName } from "@fortawesome/fontawesome-common-types";
import React from "react";
import * as styles from "./Icon.module.css";

interface IconProps {
  name: IconName;
  space?: boolean;
}

export default function Icon({ name, space }: IconProps) {
  return (
    <span className={`fa-solid fa-${name} ${space ? styles["space"] : ""}`} />
  );
}
