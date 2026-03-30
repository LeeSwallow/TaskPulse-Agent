function sameDay(a, b) {
  return (
    a.getFullYear() === b.getFullYear()
    && a.getMonth() === b.getMonth()
    && a.getDate() === b.getDate()
  )
}

function atNoon(year, month, day) {
  return new Date(year, month, day, 12, 0, 0, 0)
}

function shiftDate(date, amount) {
  const next = atNoon(date.getFullYear(), date.getMonth(), date.getDate())
  next.setDate(next.getDate() + amount)
  return next
}

export function formatMonthLabel(date) {
  return date.toLocaleDateString('en-US', {
    month: 'long',
    year: 'numeric',
  })
}

export function formatSelectedDateLabel(date) {
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    weekday: 'long',
  })
}

export function buildCalendarMonth(anchorDate, events, selectedDate) {
  const firstDay = atNoon(anchorDate.getFullYear(), anchorDate.getMonth(), 1)
  const gridStart = shiftDate(firstDay, -firstDay.getDay())
  const today = atNoon(2026, 2, 30)

  return Array.from({ length: 35 }, (_, index) => {
    const date = shiftDate(gridStart, index)
    const eventCount = events.filter(
      (event) => event.day === date.getDate() && date.getMonth() === anchorDate.getMonth(),
    ).length

    return {
      key: date.toISOString(),
      date,
      dayNumber: date.getDate(),
      eventCount,
      isCurrentMonth: date.getMonth() === anchorDate.getMonth(),
      isSelected: sameDay(date, selectedDate),
      isToday: sameDay(date, today),
      label: date.toLocaleDateString('en-US', {
        month: 'long',
        day: 'numeric',
      }),
    }
  })
}
