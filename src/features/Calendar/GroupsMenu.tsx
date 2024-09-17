import React, { ChangeEventHandler, useEffect, useRef, useState } from "react";
import { Source } from "../../groups";
import * as styles from "./GroupsMenu.module.css";

interface GroupsMenuProps {
  allIds: string[];
  /** The possible sources to choose from. */
  sources: Source[];
  /** Whether the sources are currently shown or not. */
  shown: Set<string>;
  /** Callback to set `shown`. */
  setShown: React.Dispatch<React.SetStateAction<Set<string>>>;
  /** Whether to display groups of type annexe or not. */
  showAnnexe: boolean;
  /** Callback to set `showAnnexe`. */
  setShowAnnexe: React.Dispatch<React.SetStateAction<boolean>>;
  /** The current filter. */
  titleFilter: string;
  /** Callback to set `filter`. */
  setTitleFilter: React.Dispatch<React.SetStateAction<string>>;
}

/**
 * A component that allows the user to choose from several groups.
 */
export default function GroupsMenu({ allIds, sources, shown, setShown, showAnnexe, setShowAnnexe, titleFilter: filter, setTitleFilter: setFilter }: GroupsMenuProps) {
  // deal with the "select all" checkbox
  const selectAllRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    const ref = selectAllRef.current;
    if (!ref) {
      // not yet initialized
      return;
    }

    if (shown.size === allIds.length) {
      // every group is shown
      ref.checked = true;
      ref.indeterminate = false;
    } else if (shown.size === 0) {
      // no group is shown
      ref.checked = false;
      ref.indeterminate = false;
    } else {
      // indeterminate case
      ref.checked = false;
      ref.indeterminate = true;
    }
  }, [shown, allIds]);

  const [showDetails, setShowDetails] = useState(false);

  const handleSelectAllChange: ChangeEventHandler<HTMLInputElement> = (e) => {
    const checked = e.target.checked;
    setShown(checked ? new Set(allIds) : new Set());
  };

  return (
    <div className={styles["menu"]}>
      <div className={styles["list"]}>
        <label className={styles["check"]} htmlFor="checkbox-select-all">
          <input
            id="checkbox-select-all"
            type="checkbox"
            ref={selectAllRef}
            onChange={handleSelectAllChange}
          />
          &nbsp;Tous
        </label>

        {sources.map((source) => {
          const details = `${source.parcours.toUpperCase()} ∙ ${source.year.toUpperCase()} ∙ ${source.label
            } [#${source.id}]`;

          return (
            <label
              htmlFor={`checkbox-${source.id}`}
              key={source.id}
              className={styles["check"]}
              data-shown={shown.has(source.id)}
              title={details}
              style={{
                backgroundColor: shown.has(source.id)
                  ? source.color
                  : "#bbbbbb",
                color: shown.has(source.id) ? source.textColor : "#000000",
              }}
            >
              <input
                id={`checkbox-${source.id}`}
                type="checkbox"
                checked={shown.has(source.id) ?? false}
                onChange={(e) => {
                  if (e.target.checked) {
                    setShown(currentlyShown => new Set(currentlyShown.add(source.id)));
                  }
                  else {
                    setShown(currentlyShown => {
                      currentlyShown.delete(source.id);
                      return new Set(currentlyShown);
                    });
                  }
                }}
              />
              &nbsp;
              {showDetails ? details : source.label}
            </label>
          );
        })}
      </div>

      <details className={styles["options"]}>
        <summary>Options avancées</summary>
        <label>
          <input
            type="checkbox"
            checked={showDetails}
            onChange={(e) => setShowDetails(e.target.checked)}
          />
          <div>Codes des fiches</div>
        </label>

        <label>
          <input
            type="checkbox"
            checked={showAnnexe}
            onChange={(e) => setShowAnnexe(e.target.checked)}
          />
          <div>Fiches annexes</div>
        </label>

        <label>
          <div>Filtre</div>
          <input
            type="text"
            placeholder="Algèbre..."
            value={filter}
            onChange={e => setFilter(e.target.value)}
          />
        </label>
      </details>
    </div>
  );
}
