// The entry point for the embedded app.

import React, { Suspense } from "react";
import { createRoot } from "react-dom/client";
import ErrorBoundary from "./features/Layout/ErrorBoundary";
import { filterCalendars } from "./features/Menu/CalendarWrapper";
import { Fallback } from "./features/App";
import { defaultCalendars } from "./config";
const Calendar = React.lazy(() => import("./features/Calendar"));

import "./global.css";

document.getElementById("fallback")?.remove();

const root = document.createElement("div");
document.body.appendChild(root);

// Retrieve the parcours and year parameters from the URL.
const searchParams = new URLSearchParams(window.location.search);
const parcours = searchParams.get("parcours") ?? "";
const year = searchParams.get("year") ?? "";
const calendars = defaultCalendars();
const groups = filterCalendars(calendars, parcours, year);
const reactRoot = createRoot(root);
reactRoot.render(
  <ErrorBoundary>
    {/* While the lazily loaded components are being fetched, we just display a simple message. */}
    <Suspense fallback={<Fallback />}>
      <Calendar groups={groups} bare />
    </Suspense>
  </ErrorBoundary>,
);
