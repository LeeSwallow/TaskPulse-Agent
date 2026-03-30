import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { EventForm } from '../components/event-form/EventForm.jsx'

describe('EventForm', () => {
  it('validates required fields before submit', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()

    render(<EventForm onSubmit={onSubmit} />)

    await user.clear(screen.getByLabelText(/title/i))
    await user.clear(screen.getByLabelText(/instruction/i))
    await user.click(screen.getByRole('button', { name: /save draft/i }))

    expect(onSubmit).not.toHaveBeenCalled()
    expect(screen.getByText(/title is required/i)).toBeInTheDocument()
    expect(screen.getByText(/instruction is required/i)).toBeInTheDocument()
  })

  it('switches schedule fields when weekly is selected', async () => {
    const user = userEvent.setup()

    render(<EventForm onSubmit={() => {}} />)

    expect(screen.getByLabelText(/time of day/i)).toBeInTheDocument()
    expect(screen.queryByLabelText(/run at/i)).not.toBeInTheDocument()

    await user.selectOptions(screen.getByLabelText(/schedule type/i), 'weekly')

    expect(screen.getByText(/weekdays/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/time of day/i)).toBeInTheDocument()
  })

  it('builds a weekly payload from user input', async () => {
    const user = userEvent.setup()
    const onSubmit = vi.fn()

    render(<EventForm onSubmit={onSubmit} />)

    await user.clear(screen.getByLabelText(/title/i))
    await user.type(screen.getByLabelText(/title/i), 'Weekly Ops Digest')
    await user.clear(screen.getByLabelText(/instruction/i))
    await user.type(
      screen.getByLabelText(/instruction/i),
      'Collect product updates and publish them to Slack',
    )
    await user.selectOptions(screen.getByLabelText(/schedule type/i), 'weekly')
    await user.clear(screen.getByLabelText(/time of day/i))
    await user.type(screen.getByLabelText(/time of day/i), '18:30')
    await user.click(screen.getByText('Tue'))
    await user.click(screen.getByText('Thu'))
    await user.click(screen.getByText('Send Slack'))
    await user.selectOptions(screen.getByLabelText(/notify target/i), 'slack')
    await user.click(screen.getByRole('button', { name: /save draft/i }))

    expect(onSubmit).toHaveBeenCalledTimes(1)
    expect(onSubmit).toHaveBeenCalledWith({
      title: 'Weekly Ops Digest',
      instruction: 'Collect product updates and publish them to Slack',
      schedule: {
        type: 'weekly',
        timezone: 'Asia/Seoul',
        timeOfDay: '18:30',
        daysOfWeek: [1, 2, 3, 4, 5],
      },
      allowedTools: ['web_search', 'send_slack'],
      notifyTarget: 'slack',
    })
  })
})
