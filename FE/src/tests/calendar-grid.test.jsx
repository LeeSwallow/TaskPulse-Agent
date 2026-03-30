import { fireEvent, render, screen } from '@testing-library/react'
import { describe, expect, it, vi } from 'vitest'
import { CalendarGrid } from '../components/calendar/CalendarGrid.jsx'
import { buildCalendarMonth } from '../lib/date/calendar.js'

describe('CalendarGrid', () => {
  const anchorDate = new Date('2026-03-01T09:00:00')
  const selectedDate = new Date('2026-03-30T09:00:00')
  const events = [
    { id: 'event-1', day: 30 },
    { id: 'event-2', day: 30 },
    { id: 'event-3', day: 31 },
  ]

  it('renders month cells and event counts', () => {
    const days = buildCalendarMonth(anchorDate, events, selectedDate)

    render(<CalendarGrid days={days} onSelectDate={() => {}} />)

    expect(screen.getAllByRole('gridcell')).toHaveLength(35)
    expect(screen.getAllByRole('gridcell', { name: /march 30/i })[0]).toHaveTextContent('2 events')
  })

  it('marks the selected date and emits selection on click', async () => {
    const onSelectDate = vi.fn()
    const days = buildCalendarMonth(anchorDate, events, selectedDate)

    const { container } = render(<CalendarGrid days={days} onSelectDate={onSelectDate} />)

    const march31 = container.querySelector('[aria-label="March 31"]')
    const march30 = container.querySelector('[aria-label="March 30"]')
    expect(march30).toHaveAttribute('aria-pressed', 'true')

    fireEvent.click(march31)

    expect(onSelectDate).toHaveBeenCalledTimes(1)
    expect(onSelectDate.mock.calls[0][0]).toBeInstanceOf(Date)
    expect(onSelectDate.mock.calls[0][0].getDate()).toBe(31)
  })
})
