import config from "./config.json";
import { Group } from "./groups";
import { IconName } from "@fortawesome/fontawesome-common-types";

import calendars from "../calendars.json";
import calendarsExternal from "../calendars_external.json";

/**
 * Gets the title of a parcours from `config.json`.
 * @param parcours The parcours of which we want the title.
 * @returns The title of `parcours`.
 * @todo Better error handling.
 */
export function getParcoursTitle(parcours: string): string {
  const parcoursTitles = config["parcoursTitles"];
  if (!(parcours in parcoursTitles)) {
    return "Inconnu";
  } else {
    return parcoursTitles[parcours as keyof typeof parcoursTitles];
  }
}

export function getParcoursIconName(parcours: string): IconName | null {
  const parcoursIcons = config["parcoursIcons"];
  if (!(parcours in parcoursIcons)) {
    return null;
  } else {
    return parcoursIcons[parcours as keyof typeof parcoursIcons] as IconName;
  }
}

/**
 * Returns an array of all default calendar groups.
 * @returns An array of calendar groups.
 */
export function defaultCalendars(): Group[] {
  return [
    ...calendars.map(
      (cal): Group => ({
        ...cal,
        id: cal.code.toString(),
      }),
    ),
    ...calendarsExternal,
  ];
}

/**
 * Returns an array of calendar groups for a given archive path and date.
 * The initial date is set to the given date.
 * @param archivePath The path to the archive.
 * @param archiveDate The date of the archive.
 * @returns An array of calendar groups.
 */
export function getArchiveCalendars(archivePath: string, archiveDate: string): Group[] {
  return [
    ...calendars.map(
      (cal): Group => ({
        ...cal,
        dataSubDir: archivePath,
        id: cal.code.toString(),
        // We erase the initialDate from the calendar.json file as they would override the default initialDate
        initialDate: archiveDate,
      }),
    ),
    ...calendarsExternal,
  ];
}

/**
 * Returns an array of all calendar groups for a given archive and date.
 * If `archive` is null, returns the default calendars.
 * If `manualDate` is not null, uses it as the initial date for the calendars.
 * @param archive The archive to get the calendar groups for.
 * @param manualDate The manual date to use as the initial date for the calendars.
 * @returns An array of calendar groups.
 */
export function getAllGroups(archive: string | null, manualDate: string | null): Group[] {
  if (manualDate !== null) {
    config.defaultInitialDate = manualDate;
  }

  const archiveInitialDateMap: Map<string, string> = new Map([
    ["2019-20", "2019-12-02"],
    ["2020-21", "2020-11-30"],
    ["2021-22", "2021-09-06"],
    ["2022-23", "2022-08-29"],
    ["2023-24", "2023-08-29"],
  ]);

  if (archive) {
    const archiveInitialDate = archiveInitialDateMap.get(archive);
    if (archiveInitialDate) {
      config.defaultInitialDate = (manualDate !== null) ? manualDate : archiveInitialDate;
      return getArchiveCalendars(`${archive}/`, config.defaultInitialDate);
    } else {
      throw new Error(`Archive ${archive} not found`);
    }
  }

  if (manualDate === null) {
    return defaultCalendars();
  }

  // prise en compte de la date en argument pour l'archive par défaut
  return getArchiveCalendars("", config.defaultInitialDate);
}


/** An RGB color. */
interface RGB {
  /** The red value. */
  r: number;
  /** The green value. */
  g: number;
  /** The blue value. */
  b: number;
}

/** A hue-saturation-lightness color. */
interface HSL {
  /** Hue (on a wheel, 0° = 360° = Red) */
  h: number;
  /** Saturation, 0% = gray, 100% = fully saturated. */
  s: number;
  /** Lightness: 0% = black, 100% = white, 50% = normal hue. */
  l: number;
}
type Color = RGB | HSL;

/** An RGB color representing black. */
const black: RGB = { b: 0, g: 0, r: 0 };
/** An RGB color representing white. */
const white: RGB = { b: 255, g: 255, r: 255 };

/**
 * Converts a color object to a CSS color string.
 * @param color The color object to convert.
 * @returns A CSS color string.
 */
export function colorToCSS(color: Color) {
  if ("r" in color) {
    // RGB
    const { r, g, b } = color;
    const parsed = [r, g, b].map((n) => {
      const s = n.toString(16);
      return "0".repeat(2 - s.length) + s;
    });
    return `#${parsed.join("")}`;
  } else {
    // HSL
    const { h, s, l } = color;
    return `hsl(${h}, ${s}%, ${l}%)`;
  }
}

/**
 * Gets a background color from the palette. Groups of the same type have the same color. Annexe groups are black.
 * @param group The group to be displayed.
 * @param index The (cyclic) index of the color.
 */
export function getBgColor(group: Group, index: number): Color {
  if (group.annexe) {
    return black;
  } else {
    return config.bgPalette[index % config.bgPalette.length] ?? black;
  }
}

/**
 * Computes an appropriate foreground color (either black or white) depending on a brightness threshold.
 * @param group The group to be displayed
 * @param index The (cyclic) index of the color.
 * @returns An hexadecimal RGB representation of the foreground color.
 * @see https://computergraphics.stackexchange.com/questions/5085/light-intensity-of-an-rgb-value
 */
export function getFgColor(group: Group, index: number): RGB {
  const color = getBgColor(group, index);
  if ("r" in color) {
    const { r, g, b } = color;
    const brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b;
    return brightness >= 128 ? black : white;
  } else {
    return color.l >= 50 ? black : white;
  }
}
