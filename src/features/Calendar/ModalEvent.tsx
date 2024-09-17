import { EventApi } from "@fullcalendar/core";
import React, { useCallback, useEffect } from "react";

import { getParcoursTitle } from "../../config";
import { Source } from "../../groups";
import * as styles from "./ModalEvent.module.css";

interface ModalEventProps {
  /** The event to be shown. */
  event: EventApi;
  /** A function that will be called when the event is closed. */
  onClose: () => void;
  /** The sources of the event. */
  source: Source | undefined;
}

/**
 * A modal ("pop-up") event that appears when an event is clicked.
 */
export default function ModalEvent({ event, onClose, source }: ModalEventProps) {
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.code === "Escape") {
        onClose();
      }
    }, [onClose]);

  useEffect(() => {
    document.addEventListener("keydown", handleKeyDown);
    return () => {
      document.removeEventListener("keydown", handleKeyDown);
    };
  }, [handleKeyDown]);

  return (
    <>
      <div
        className={styles["modal"]}
        onClick={(e) => {
          // checks if we are clicking on the div itself but not its content
          if (e.currentTarget === e.target) {
            onClose();
          }
        }}
      >
        <article
          style={{
            backgroundColor: source?.color,
            color: source?.textColor,
          }}
        >
          <header>
            {source?.year.toUpperCase()} {getParcoursTitle(source?.parcours ?? "")} &middot; Groupe {source?.label}
          </header>
          <button onClick={() => onClose()}>&times;</button>
          <div>
            <h2>{event.title}</h2>
            <p>
              <em>{event.extendedProps["location"]}</em>
              <br />
              {event.start?.toLocaleDateString("fr-FR", {
                dateStyle: "full",
              })}{" "}
              | {/* Fullcalendar ne comprend pas les timezones. Point. */}
              {new Date(event.startStr).toLocaleTimeString("fr-FR", {
                timeStyle: "short",
              })}
              &ndash;
              {new Date(event.endStr).toLocaleTimeString("fr-FR", {
                timeStyle: "short",
              })}
            </p>
            {source?.annexe && (
              <p>⚠️ Cette réservation est obsolète !</p>
            )}
          </div>
          <footer className="text-xs tracking-tight">
            {event.extendedProps["description"]}
          </footer>
        </article>
      </div>
    </>
  );
}
