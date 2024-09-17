// The entry point for the app in "single" mode.

import React, { Suspense } from "react";
import { createRoot } from "react-dom/client";
import ErrorBoundary from "./features/Layout/ErrorBoundary";
import { filterCalendars } from "./features/Menu/CalendarWrapper";

const Calendar = React.lazy(() => import("./features/Calendar"));

import "./global.css";
import { defaultCalendars } from "./config";

const calendars = defaultCalendars();

// cherche tous les élements qui ressemblent à :
// <div class="root-edt" data-parcours="maths" data-year="l1" />
// et affiche le calendrier dedans
for (const root of Array.from(document.querySelectorAll<HTMLElement>(".root-edt"))) {
  const { year, parcours } = root.dataset;
  if (!year || !parcours) {
    throw new Error("Root element without parcours and/or year!");
  }
  const reactRoot = createRoot(root);
  const groups = filterCalendars(calendars, parcours, year);
  reactRoot.render(
    <ErrorBoundary>
      <Suspense
        fallback={
          <div>
            Chargement de {parcours} &ndash; {year}...
          </div>
        }
      >
        <Calendar groups={groups} bare />
      </Suspense>
    </ErrorBoundary>,
  );

}
