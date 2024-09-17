import React from "react";
import * as styles from "./ErrorBoundary.module.css";

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

/**
 * An error boundary that displays a message when something went wrong.
 * @see https://reactjs.org/docs/error-boundaries.html
 */
export default class ErrorBoundary extends React.Component<ErrorBoundaryProps> {
  override state: ErrorBoundaryState = {
    hasError: false,
  };

  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
    };
  }

  static getDerivedStateFromError(_error: unknown): ErrorBoundaryState {
    return {
      hasError: true,
    };
  }

  override componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error("Uncaught error", error);
    console.error(errorInfo);
  }

  public override render() {
    if (this.state.hasError) {
      return <ErrorPage />;
    } else {
      return this.props.children;
    }
  }
}
function ErrorPage() {
  return <div className={styles["error"]}>
    <h1>Désolé... Une erreur s&rsquo;est produite ! ☹</h1>
    <p>
      <a href="/">Retour à l&rsquo;accueil</a>
    </p>
  </div>;
}
