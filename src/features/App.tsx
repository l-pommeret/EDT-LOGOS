import React, { Suspense } from "react";
import { Navigate, Route, Routes } from "react-router-dom";
import { getAllGroups } from "../config";
import Layout from "./Layout";
import CalendarWrapper from "./Menu/CalendarWrapper";
import { routes, routeParams } from "./routing";
import * as styles from "./App.module.css";

// The following components are lazily loaded to save the user having to download the full app just to display one page.
const Menu = React.lazy(() => import("./Menu"));
const Manual = React.lazy(() => import("./Manual"));
const ManualMenu = React.lazy(() => import("./Manual/Menu"));
const Help = React.lazy(() => import("./Help"));

export function Fallback() {
  return <p className={styles["fallback"]}>
    <span className={styles["spinner"]} />
    Chargement de l&rsquo;interface...
  </p>;
}

function NotFound() {
  return <div className={styles["not-found"]}>
    <p>
      Erreur : page non trouvée !
    </p>
    <p>
      <a href="/">Retour à l&rsquo;accueil</a>
    </p>
  </div>;
}

/**
 * The full app. Contains three main pages:
 * - `/` and `/parcours` will allow a user to choose a single parcours/year combo from a list.
 * - `/manuel` allows a user to select an arbitrary list of groups.
 * - `/aide` is a help page.
 */
export default function App() {
  // Retrieve the archive and date parameters from the URL.
  const searchParams = new URLSearchParams(window.location.search);
  const archive = searchParams.get("archive");
  const manualDate = searchParams.get("date");
  // Retrieve all groups from the config file.
  const allGroups = getAllGroups(archive, manualDate);

  return (
    <Layout>
      {/* While the lazily loaded components are being fetched, we just display a simple message. */}
      <Suspense fallback={<Fallback />}>
        <Routes>
          <Route path="/">

            <Route
              // The index gets redirected to /parcours.
              index
              // We use `replace` to avoid the "back button problem". Without replace, if someone goes to the index, they are redirected to /parcours, and going back in the history will bring them back to the index, which will redirect them to /parcours, and so on.
              element={<Navigate to={routes.parcours} replace />}
            />

            <Route
              path={`${routes.parcours}/:${routeParams.parcours}?`}
              element={<Menu allGroups={allGroups} />}
            >
              <Route
                path={`:${routeParams.year}/:${routeParams.selectedGroups}?`}
                element={<CalendarWrapper allGroups={allGroups} />}
              />
            </Route>

            {/* Manual choice */}
            <Route path={routes.manuel}>
              <Route
                index
                element={<ManualMenu allGroups={allGroups} />}
              />
              <Route
                path={`:${routeParams.selectedGroups}`}
                element={<Manual allGroups={allGroups} />}
              />
            </Route>

            {/* Help component */}
            <Route
              path={routes.aide}
              element={<Help />}
            />

            {/* 404 error */}
            <Route
              path="*"
              element={<NotFound />}
            />
          </Route>
        </Routes>
      </Suspense>
    </Layout >
  );
}
