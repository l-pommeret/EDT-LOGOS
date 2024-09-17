import { EventApi, EventContentArg } from "@fullcalendar/core";
import frLocale from "@fullcalendar/core/locales/fr";
import dayGridPlugin from "@fullcalendar/daygrid";
import iCalendarPlugin from "@fullcalendar/icalendar";
import listPlugin from "@fullcalendar/list";
import FullCalendar from "@fullcalendar/react";
import timeGridPlugin from "@fullcalendar/timegrid";
import React, { useCallback, useDeferredValue, useEffect, useMemo, useRef, useState } from "react";

import config from "../../config.json";
import { Group, groupToSource, Source } from "../../groups";
import Footer from "./Footer";
import GroupsMenu from "./GroupsMenu";
import ModalEvent from "./ModalEvent";

/**
 * Convert an event to HTML.
 * @see https://fullcalendar.io/docs/event-render-hooks
 */
function renderEventContent({ event: { title, extendedProps: { location } } }: EventContentArg) {
  return (
    <>
      {title}
      <br />
      <em>{location}</em>
    </>
  );
}

export interface CalendarProps {
  /** The groups that should be included in the calendar. */
  groups: Group[];
  /** A list of pre-selected group, separated by "+". Does not change on user input. */
  selectedGroups?: string;
  /** If true, then do not render extra elements around the calendar (useful for embedding in another document). */
  bare?: boolean;
}

/**
 * Renders a calendar composed of several groups, together with its title.
 */
export default function Calendar({ groups, selectedGroups, bare }: CalendarProps) {
  const [showAnnexe, setShowAnnexe] = useState(false);

  const mainGroups = useMemo(() => groups.filter(g => !g.annexe), [groups]);
  const annexeGroups = useMemo(() => groups.filter(g => g.annexe), [groups]);
  const filteredGroups = useMemo(() =>
    showAnnexe ? mainGroups.concat(annexeGroups) : mainGroups,
    [showAnnexe, mainGroups, annexeGroups]);

  const allIds = useMemo(() => filteredGroups.map(g => g.id), [filteredGroups]);

  /**
   * The configuration of the sources for FullCalendar, determined from `groups`.
   */
  const sources: Source[] = useMemo(() => filteredGroups.map(groupToSource), [filteredGroups]);

  /**
   * Whether a group is hidden or not.
   * The key is the (numerical) code of a group.
   */
  const [shownGroups, setShownGroups] = useState(new Set<string>());

  /**
   * The event currently shown in a modal, or `null` if no event is shown.
   */
  const [currentEvent, setCurrentEvent] = useState<EventApi | null>(null);

  /**
   * The current filter.
   */
  const [titleFilter, setTitleFilter] = useState("");

  /**
   * A deferred version of `titleFilter`.
   * Useful to avoid lag when typing in the input.
   */
  const deferredTitleFilter = useDeferredValue(titleFilter);

  return (
    <>
      {currentEvent && (
        <ModalEvent
          event={currentEvent}
          source={sources.find(s => s.id === currentEvent.source?.id)}
          onClose={() => setCurrentEvent(null)}
        />
      )}

      <div>
        <GroupsMenu
          allIds={allIds}
          sources={sources}
          shown={shownGroups}
          setShown={setShownGroups}
          showAnnexe={showAnnexe}
          setShowAnnexe={setShowAnnexe}
          titleFilter={titleFilter}
          setTitleFilter={setTitleFilter}
        />

        <CalendarChild
          groups={filteredGroups}
          selectedGroups={selectedGroups}
          setCurrentEvent={setCurrentEvent}
          setShownGroups={setShownGroups}
          shownGroups={shownGroups}
          sources={sources}
          titleFilter={deferredTitleFilter}
        />

        <Footer sources={sources} shown={shownGroups} bare={bare ?? false} />
      </div>
    </>
  );
}

interface CalendarChildProps {
  groups: Group[];
  selectedGroups?: string;
  setCurrentEvent: React.Dispatch<React.SetStateAction<EventApi | null>>;
  setShownGroups: React.Dispatch<React.SetStateAction<Set<string>>>;
  shownGroups: Set<string>;
  sources: Source[];
  titleFilter: string;
}

/**
 * A child component of `Calendar`.
 * This is a separate component to avoid re-rendering the whole calendar when the user types in the filter input.
 */
function CalendarChild({ groups, selectedGroups, setCurrentEvent, shownGroups, setShownGroups, sources, titleFilter }: CalendarChildProps) {
  /**
   * The filter, with accents removed and converted to lowercase.
   */
  const normalizedTitleFilter = useMemo(() => removeAccents(titleFilter.toLowerCase()), [titleFilter]);

  /**
   * A callback to determine whether an event should be displayed or not.
   * This is used to filter events based on the filter input.
   */
  const eventDisplayProp = useCallback((event: EventApi) => {
    if (!normalizedTitleFilter || removeAccents(event.title.toLowerCase()).includes(normalizedTitleFilter)) {
      return "auto";
    } else {
      return "none";
    }
  }, [normalizedTitleFilter]);

  /**
   * A reference to the FullCalendar.
   * Useful to get the API in useEffect's.
   */
  const calendarRef = useRef<FullCalendar>(null);

  // When groups changes...
  useEffect(() => {
    // remove any event shown in the modal.
    setCurrentEvent(null);
    // set an initial value for shown
    setShownGroups(
      new Set(
        sources
          .filter((g) =>
            // Fix pour archive en argument ET présélections de groupes avec +
            selectedGroups
              // if groups are pre-selected from URL parameters, only show these one by default at the beginning
              ? selectedGroups.split("+").includes(g.id)
              // otherwise, show everything except "annexe" groups
              : !g.annexe,
          )
          .map(g => g.id),
      ),
    );
  }, [sources, selectedGroups, setCurrentEvent, setShownGroups]);

  // when groups and/or shown groups change, add or remove sources using the FullCalendar API.
  useEffect(() => {
    if (!calendarRef.current) {
      return;
    }
    const api = calendarRef.current.getApi();

    for (const src of api.getEventSources()) {
      if (!shownGroups.has(src.id)) {
        // if the source is not shown, we remove it
        src.remove();
      }
    }

    for (const src of sources) {
      if (!shownGroups.has(src.id)) {
        // if the source is not shown, we remove it
        // note that with ?., if no source is found, nothing happens
        api.getEventSourceById(src.id)?.remove();
      } else if (!api.getEventSourceById(src.id)) {
        // if the source is not here, add it
        api.addEventSource(src);
      }
    }
  }, [shownGroups, sources]);

  useEffect(() => {
    if (!calendarRef.current) {
      return;
    }
    const api = calendarRef.current.getApi();

    for (const event of api.getEvents()) {
      event.setProp("display", eventDisplayProp(event));
    }
  }, [titleFilter, eventDisplayProp]);

  const initialDate = useMemo(() => {
    const today = new Date();
    const defaultInitialDate = new Date(config.defaultInitialDate);
    const manualDate = groups
      .map((g) => new Date(g.initialDate ?? ((today < defaultInitialDate) ? defaultInitialDate : today)))
      .reduce((previous, current) =>
        !current || previous !== ((today < defaultInitialDate) ? defaultInitialDate : today)
          ?
          previous
          : current,
        ((today < defaultInitialDate) ? defaultInitialDate : today),
      );

    return (manualDate);

  }, [groups]);

  // // when groups changes, use the API to go to that date
  // useEffect(() => {
  //   /* apres un an d'utilisation, cette fonctionnalité de retour a la date par défaut
  //   lors  du changement de bouton n'est pas pratique, il vaut mieux laisser la date courante.

  //   const api = calendarRef.current?.getApi();
  //   api?.gotoDate(initialDate);
  //   */
  // }, [groups]);

  return (
    <FullCalendar
      ref={calendarRef}
      plugins={[
        /* interactionPlugin,*/
        dayGridPlugin,
        timeGridPlugin,
        listPlugin,
        iCalendarPlugin,
      ]}
      headerToolbar={{
        center: "title",
        left: "prev,next today",
        right: "timeGridWeek,timeGridDay,listWeek",
      }}

      /*
        Certains calendriers external sont en UTC. Il vaut mieux laisser la
        timeZone par défaut qui semble être "local"
        cela ne pose plus de PB pour nos calendriers ADE car on a ajoute des
        TZID=Europe/Paris: a tous les horaires envoyés par ADE.
        timeZone aux calendriers envoyés par ADE.
      */
      timeZone="local"

      locale={frLocale}
      initialDate={initialDate}
      initialView="timeGridWeek"
      // firstDay: 1,
      hiddenDays={[0]}
      // can click day/week names to navigate views
      navLinks={true}
      editable={false}
      allDaySlot={false}
      // allow "more" link when too many events
      dayMaxEvents={true}
      contentHeight="auto"
      slotMinTime="08:00:00"
      slotMaxTime="20:00:00"

      eventContent={(content) => renderEventContent(content)}
      eventClick={({ event }) => setCurrentEvent(event)}
      eventDidMount={({ event }) => {
        event.setProp("display", eventDisplayProp(event));
      }}
    />
  );
}

/**
 * Converts accented characters into unaccented ones.
 * @see https://stackoverflow.com/a/37511463
 */
export function removeAccents(s: string): string {
  return s.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}
