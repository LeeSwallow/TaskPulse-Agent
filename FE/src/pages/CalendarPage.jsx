import { useState } from 'react'
import { CalendarGrid } from '../components/calendar/CalendarGrid.jsx'
import { EventForm } from '../components/event-form/EventForm.jsx'
import { buildCalendarMonth, formatMonthLabel, formatSelectedDateLabel } from '../lib/date/calendar.js'

const seededEvents = [
  {
    id: 'event-1',
    title: 'Morning Briefing',
    day: 30,
    detail: '09:00 daily · web_search, send_slack',
  },
  {
    id: 'event-2',
    title: 'Weekly Ops Digest',
    day: 31,
    detail: '18:30 weekly · dashboard delivery',
  },
  {
    id: 'event-3',
    title: 'Backlog Sweep',
    day: 26,
    detail: '14:00 once · review queue',
  },
]

const recentExecutions = [
  {
    title: 'Workspace Summary',
    detail: 'Succeeded · 08:55',
  },
  {
    title: 'Market Watch Agent',
    detail: 'Running · started 2m ago',
  },
]

const monthAnchor = new Date('2026-03-01T09:00:00')

export function CalendarPage() {
  const [selectedDate, setSelectedDate] = useState(new Date('2026-03-30T09:00:00'))
  const [draftPayload, setDraftPayload] = useState(null)

  const calendarDays = buildCalendarMonth(monthAnchor, seededEvents, selectedDate)
  const selectedEvents = seededEvents.filter(
    (event) => event.day === selectedDate.getDate(),
  )

  return (
    <main className="app-shell" data-testid="app-shell">
      <header className="app-shell__header">
        <div className="app-shell__brand">
          <span className="app-shell__eyebrow">TaskPulse Agent</span>
          <h1 className="app-shell__title">Calendar Console</h1>
        </div>
        <div className="app-shell__status" aria-label="runtime status">
          <span className="app-shell__status-dot" aria-hidden="true" />
          Calendar-first planning · Seoul workspace
        </div>
      </header>

      <section className="calendar-page">
        <section
          className="calendar-page__main panel calendar-hero"
          aria-label="calendar region"
        >
          <div className="calendar-hero__topline">
            <div>
              <p className="app-shell__eyebrow">{formatMonthLabel(monthAnchor)}</p>
              <h2 className="calendar-hero__month">Primary scheduling surface</h2>
              <p className="calendar-hero__meta">
                The calendar is the base interaction model. Date selection drives
                event inspection, composition, and execution context.
              </p>
            </div>
            <div className="calendar-hero__badge">
              Selected date · {formatSelectedDateLabel(selectedDate)}
            </div>
          </div>

          <CalendarGrid
            days={calendarDays}
            onSelectDate={setSelectedDate}
          />
        </section>

        <aside className="calendar-page__sidebar sidebar-stack">
          <section className="panel detail-card" aria-label="detail panel">
            <h2 className="detail-card__title">{formatSelectedDateLabel(selectedDate)}</h2>
            <p className="detail-card__copy">
              Date-driven event context. The selected calendar cell is the source
              of truth for the panel state.
            </p>
            {selectedEvents.length > 0 ? (
              <ul className="detail-card__event-list">
                {selectedEvents.map((event) => (
                  <li key={event.id} className="detail-card__event">
                    <h3>{event.title}</h3>
                    <p>{event.detail}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <div className="detail-card__empty">No scheduled events on this date.</div>
            )}
          </section>

          <section className="panel composer-card" aria-label="event composer">
            <div className="composer-card__header">
              <h2 className="composer-card__title">Event Composer</h2>
              <p className="composer-card__copy">
                Shape the scheduling payload before wiring it to the backend API.
              </p>
            </div>
            <EventForm onSubmit={setDraftPayload} />
            {draftPayload ? (
              <div className="composer-card__preview">
                <p className="composer-card__preview-label">Draft payload ready</p>
                <pre>{JSON.stringify(draftPayload, null, 2)}</pre>
              </div>
            ) : null}
          </section>

          <section className="panel feed-card" aria-label="execution feed">
            <h2 className="feed-card__title">Recent Executions</h2>
            <p className="feed-card__copy">
              Runtime summaries remain adjacent to the calendar so schedule and
              outcome stay in the same operating view.
            </p>
            <ul className="feed-card__list">
              {recentExecutions.map((execution) => (
                <li key={execution.title} className="feed-card__item">
                  <h3>{execution.title}</h3>
                  <p>{execution.detail}</p>
                  <span className="feed-card__status">Live telemetry ready</span>
                </li>
              ))}
            </ul>
          </section>
        </aside>
      </section>
    </main>
  )
}
