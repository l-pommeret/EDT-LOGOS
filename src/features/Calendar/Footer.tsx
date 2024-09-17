import React from "react";
import { Link } from "react-router-dom";
import { Source } from "../../groups";
import * as styles from "./Footer.module.css";

interface FooterProps {
  /** An array of sources to display. */
  sources: Source[];
  /** A boolean indicating whether to display only the iCal data or also the links to permanent URLs. */
  bare: boolean;
  /** A map of source IDs to booleans indicating whether each source should be displayed. */
  shown: Set<string>;
}

/**
 * A component that displays links to permanent URLs and iCal data for a list of sources.
 */
export default function Footer({ sources, shown, bare }: FooterProps) {
  const filteredSources = sources.filter((g) => shown.has(g.id));


  return (
    <footer className={styles["footer"]}>
      {!bare && (
        <>
          <Permalink sources={filteredSources} />
          <div>
            <div>Liens permanents vers les fiches individuelles :</div>
            {sources.map(({ parcours, year, label, id }) => (
              <div key={id}>
                <Link to={`/parcours/${parcours}/${year}/${id}`} >
                  {`#${label}`}
                </Link>
              </div>
            ))}
          </div>
        </>
      )}
      <div>
        <div>
          Données au format <code>ICal</code> :
        </div>
        {sources.map((g) => (
          <div key={g.id}>
            <a href={g.url} title={`Fichier ical pour ${g.label} (identifiant : ${g.id}).`}>
              {`${g.label}.ics`}
            </a>
          </div>
        ))}
      </div>
    </footer>
  );
}

function Permalink({ sources }: { sources: Source[]; }) {
  const parcours = new Set(sources.map(g => g.parcours));
  const year = new Set(sources.map(g => g.year));
  const groups = (sources.map((g) => g.id)).join("+");

  function format(link: string) {
    return (
      <p>
        <Link to={link}>
          → Lien permanent vers la sélection actuelle.
        </Link>
      </p>
    );
  }

  if (parcours.size === 1 && year.size === 1) {
    const [oneParcours] = parcours;
    const [oneYear] = year;
    return format(`/parcours/${oneParcours}/${oneYear}/${groups}`);
  } else {
    return format(`/manuel/${groups}`);
  }
}
