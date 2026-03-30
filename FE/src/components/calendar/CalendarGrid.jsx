const weekDays = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

export function CalendarGrid({ days, onSelectDate }) {
  return (
    <div className="calendar-grid" role="grid">
      {weekDays.map((weekday) => (
        <div key={weekday} className="calendar-grid__weekday" role="columnheader">
          {weekday}
        </div>
      ))}
      {days.map((day) => (
        <button
          key={day.key}
          type="button"
          className={[
            'calendar-grid__cell',
            day.isCurrentMonth ? '' : 'calendar-grid__cell--outside',
            day.isToday ? 'calendar-grid__cell--today' : '',
            day.isSelected ? 'calendar-grid__cell--selected' : '',
          ].join(' ').trim()}
          role="gridcell"
          aria-label={day.label}
          aria-pressed={day.isSelected}
          onClick={() => onSelectDate(day.date)}
        >
          <strong className="calendar-grid__cell-day">{day.dayNumber}</strong>
          <span className="calendar-grid__cell-note">
            {day.eventCount > 0 ? `${day.eventCount} event${day.eventCount > 1 ? 's' : ''}` : 'No events'}
          </span>
        </button>
      ))}
    </div>
  )
}
