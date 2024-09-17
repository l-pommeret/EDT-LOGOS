import { colorToCSS, getBgColor, getFgColor } from "./config";

import * as styles from "./features/Calendar/OurCalendar.module.css";

/** The type of a group that either exists in ADE or in an external server. */
export interface Group {
  /** The ADE code of the group. */
  id: string;
  /** An external URL for the group.
   * @deprecated Currently unused due to CORS issues. */
  url?: string;
  /** Subfolder where the calendar data is stored (for archives)
   *  either empty or ends the dir with a /  */
  dataSubDir?: string;
  /** A friendly name for the group. */
  label: string;
  /** The parcours to which a group belongs.
   * @example "maths", "miashs"
   */
  parcours: string;
  /** The year to which a group belongs.
   * @example "l1", "l2"
  */
  year: string;
  /** The earliest date that needs to be displayed for the group. */
  initialDate?: string;
  /** Whether the group is considered accessory or not. */
  annexe?: boolean;
}

/** A source to be fed to FullCalendar. */
export interface Source {
  /** Unique identifier: either the string representation of the ADE group, or an arbitrary id. */
  id: string;
  /** The URL at which the source can be fetched, either a relative or an absolute one. */
  url: string;
  /** The format: always "ics" for now. */
  format: "ics";
  /** How the source should be displayed in FullCalendar.
   * @see https://fullcalendar.io/docs/eventDisplay
   */
  display: "auto" | "block" | "list-item" | "background" | "inverse-background" | "none";
  /** The background color of events from the source. */
  color: string;
  /** The color of the text of events from the source. */
  textColor: string;
  /** An extra class to add to the events from the source. */
  className: string;
  /** Extra data: whether the source is considered auxiliary or not. */
  annexe: boolean;
  /** Extra data: a friendly name for the source (group name). */
  label: string;
  /** Extra data: the parcours (maths, MIASHS...) to which the source belongs. */
  parcours: string;
  /** Extra data: the year (l1, l2...) to which the source belongs. */
  year: string;
}

/** The path to the directory where the calendar data is stored. */
const dataPath = process.env["DATA_PATH"] ?? "/data/";

/**
 * Converts a group to a source.
 * @param group The group to be converted.
 * @param index The index of the group in the overall sequence to which is belongs. Useful for determining the color.
 */
export function groupToSource(group: Group, index: number): Source {
  return {
    annexe: group.annexe ?? false,
    className: `${styles["source"]} ${group.annexe ? styles["dashed"] : ""}`,
    color: colorToCSS(getBgColor(group, index)),
    display: "auto",
    format: "ics",
    id: group.id,
    label: group.label,
    parcours: group.parcours,
    textColor: colorToCSS(getFgColor(group, index)),
    url: `${dataPath}${group.dataSubDir ? group.dataSubDir : ""}${group.id}.ics`,
    year: group.year,
  };
}
