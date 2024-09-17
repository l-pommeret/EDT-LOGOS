import React, { useMemo, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getParcoursTitle } from "../../config";
import { Group } from "../../groups";

import * as styles from "./Menu.module.css";

interface MenuProps {
  /** All available groups */
  allGroups: Group[];
}

/** Component for displaying a manual selection menu for choosing groups. */
export default function Menu({ allGroups }: MenuProps) {
  // The codes that are currently selected
  const [selected, setSelected] = useState(new Map<string, boolean>());
  const [formError, setFormError] = useState<string>();

  const navigate = useNavigate();

  /** List of all parcours. */
  const parcours = useMemo(() =>
    Array.from(new Set(allGroups.map(g => g.parcours))).sort(),
    [allGroups]);

  return (
    <div>
      <h1>Choix manuel</h1>

      <p>
        Choisissez manuellement des groupes en naviguant vers une URL formatée
        comme <code>/manuel/XXXX+YYYY+ZZZZ</code> où <code>XXXX</code>,{" "}
        <code>YYYY</code> et <code>ZZZZ</code> sont les codes ADE des formations
        souhaitées. Vous pouvez mettre un nombre arbitraire de codes. Vous
        pouvez aussi utiliser le formulaire suivant :
      </p>
      <form
        className={styles["choice"]}
        onSubmit={(e) => {
          e.preventDefault();
          const selectedList = allGroups
            .filter((cal) => selected.get(cal.id))
            .map((cal) => cal.id);
          if (selectedList.length > 0) {
            navigate(`/manuel/${selectedList.join("+")}`);
          } else {
            setFormError("Choisissez au moins un groupe !");
          }
        }}
      >
        <div className={styles["list"]}>
          {parcours.map((parcours) => {
            const filteredCalendars = allGroups.filter(cal => cal.parcours === parcours);
            const years = Array.from(new Set(filteredCalendars.map(cal => cal.year))).sort();

            return (
              <details key={parcours}>
                <summary>{getParcoursTitle(parcours)}</summary>
                {years.map((year) => (
                  <React.Fragment key={year}>
                    <strong>{year.toUpperCase()}</strong>
                    {filteredCalendars
                      .filter((cal) => cal.year === year)
                      .sort((cal1, cal2) =>
                        cal1.label.localeCompare(cal2.label),
                      )
                      .map((cal) => (
                        <label htmlFor={parcours + cal.id} key={cal.id}>
                          <input
                            type="checkbox"
                            id={parcours + cal.id}
                            checked={selected.get(cal.id)}
                            onChange={(e) =>
                              setSelected((map) =>
                                map.set(cal.id, e.target.checked),
                              )
                            }
                          />
                          &nbsp;
                          {cal.label}
                        </label>
                      ))}
                  </React.Fragment>
                ))}
              </details>
            );
          })}
        </div>
        {formError && <p data-error>{formError}</p>}
        <button>Voir les calendriers des groupes sélectionnés</button>
      </form>
      <p>
        Pour plus d&rsquo;explications, référez-vous à{" "}
        <Link to="/aide">l&rsquo;aide en ligne</Link>.
      </p>
    </div>
  );
}
