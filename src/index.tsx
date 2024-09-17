// The entry point for the full app.

import React from "react";
import { createRoot } from "react-dom/client";
import App from "./features/App";

import "./global.css";

import "@fortawesome/fontawesome-free/css/fontawesome.css";
import "@fortawesome/fontawesome-free/css/solid.css";

document.getElementById("fallback")?.remove();

const root = document.createElement("div");
document.body.appendChild(root);

// The entry point for React. Doesn't need to be touched.
const reactRoot = createRoot(root);
reactRoot.render(<App />);
