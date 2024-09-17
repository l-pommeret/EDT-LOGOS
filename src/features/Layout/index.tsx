import React from "react";
import { HashRouter as Router } from "react-router-dom";
import ErrorBoundary from "./ErrorBoundary";
import * as styles from "./Layout.module.css";
import { Navbar } from "./Navbar";

interface LayoutProps {
  children: React.ReactNode;
}

/**
 * Layout component that wraps the application content with a navbar and error boundary.
 */
export default function Layout({ children }: LayoutProps) {
  return (
    <ErrorBoundary>
      <div className={styles["wrapper"]}>
        <Router>
          <Navbar />
          <main className={styles["root"]}>
            {children}
          </main>
        </Router>
        <footer className={styles["footer"]}>
          Emplois du temps de l&rsquo;UFR de Mathématiques. <a href="https://gitlab.math.univ-paris-diderot.fr/molin/ical-ufr">Code source.</a>
        </footer>
      </div>
    </ErrorBoundary>
  );
}
