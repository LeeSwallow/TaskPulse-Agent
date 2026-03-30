import { useState } from 'react'

const toolOptions = [
  { value: 'web_search', label: 'Web Search' },
  { value: 'send_slack', label: 'Send Slack' },
  { value: 'dashboard', label: 'Dashboard' },
]

const weekdayOptions = [
  { value: 1, label: 'Mon' },
  { value: 2, label: 'Tue' },
  { value: 3, label: 'Wed' },
  { value: 4, label: 'Thu' },
  { value: 5, label: 'Fri' },
]

function buildInitialState(initialValues) {
  return {
    title: initialValues?.title ?? '',
    instruction: initialValues?.instruction ?? '',
    scheduleType: initialValues?.schedule?.type ?? 'daily',
    runAt: initialValues?.schedule?.runAt ?? '2026-03-31T09:00',
    timeOfDay: initialValues?.schedule?.timeOfDay ?? '09:00',
    daysOfWeek: initialValues?.schedule?.daysOfWeek ?? [1, 3, 5],
    timezone: initialValues?.schedule?.timezone ?? 'Asia/Seoul',
    allowedTools: initialValues?.allowedTools ?? ['web_search'],
    notifyTarget: initialValues?.notifyTarget ?? 'dashboard',
  }
}

function buildPayload(formState) {
  const baseSchedule = {
    type: formState.scheduleType,
    timezone: formState.timezone,
  }

  if (formState.scheduleType === 'once') {
    return {
      title: formState.title.trim(),
      instruction: formState.instruction.trim(),
      schedule: {
        ...baseSchedule,
        runAt: formState.runAt,
      },
      allowedTools: formState.allowedTools,
      notifyTarget: formState.notifyTarget,
    }
  }

  if (formState.scheduleType === 'weekly') {
    return {
      title: formState.title.trim(),
      instruction: formState.instruction.trim(),
      schedule: {
        ...baseSchedule,
        timeOfDay: formState.timeOfDay,
        daysOfWeek: formState.daysOfWeek,
      },
      allowedTools: formState.allowedTools,
      notifyTarget: formState.notifyTarget,
    }
  }

  return {
    title: formState.title.trim(),
    instruction: formState.instruction.trim(),
    schedule: {
      ...baseSchedule,
      timeOfDay: formState.timeOfDay,
    },
    allowedTools: formState.allowedTools,
    notifyTarget: formState.notifyTarget,
  }
}

export function EventForm({ initialValues, onSubmit }) {
  const [formState, setFormState] = useState(() => buildInitialState(initialValues))
  const [errors, setErrors] = useState({})

  function updateField(name, value) {
    setFormState((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function toggleAllowedTool(tool) {
    setFormState((current) => ({
      ...current,
      allowedTools: current.allowedTools.includes(tool)
        ? current.allowedTools.filter((item) => item !== tool)
        : [...current.allowedTools, tool],
    }))
  }

  function toggleWeekday(day) {
    setFormState((current) => ({
      ...current,
      daysOfWeek: current.daysOfWeek.includes(day)
        ? current.daysOfWeek.filter((item) => item !== day)
        : [...current.daysOfWeek, day].sort((left, right) => left - right),
    }))
  }

  function handleSubmit(event) {
    event.preventDefault()

    const nextErrors = {}

    if (!formState.title.trim()) {
      nextErrors.title = 'Title is required'
    }

    if (!formState.instruction.trim()) {
      nextErrors.instruction = 'Instruction is required'
    }

    if (formState.scheduleType === 'weekly' && formState.daysOfWeek.length === 0) {
      nextErrors.daysOfWeek = 'Select at least one weekday'
    }

    if (formState.allowedTools.length === 0) {
      nextErrors.allowedTools = 'Select at least one allowed tool'
    }

    setErrors(nextErrors)

    if (Object.keys(nextErrors).length > 0) {
      return
    }

    onSubmit(buildPayload(formState))
  }

  return (
    <form className="event-form" onSubmit={handleSubmit} aria-label="event composer form">
      <div className="event-form__grid">
        <label className="event-form__field">
          <span>Title</span>
          <input
            name="title"
            value={formState.title}
            onChange={(event) => updateField('title', event.target.value)}
            placeholder="Morning market scan"
          />
          {errors.title ? <strong className="event-form__error">{errors.title}</strong> : null}
        </label>

        <label className="event-form__field event-form__field--full">
          <span>Instruction</span>
          <textarea
            name="instruction"
            value={formState.instruction}
            onChange={(event) => updateField('instruction', event.target.value)}
            rows="4"
            placeholder="Summarize yesterday's market and post to dashboard"
          />
          {errors.instruction ? (
            <strong className="event-form__error">{errors.instruction}</strong>
          ) : null}
        </label>

        <label className="event-form__field">
          <span>Schedule Type</span>
          <select
            name="scheduleType"
            value={formState.scheduleType}
            onChange={(event) => updateField('scheduleType', event.target.value)}
          >
            <option value="once">Once</option>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
          </select>
        </label>

        <label className="event-form__field">
          <span>Timezone</span>
          <input
            name="timezone"
            value={formState.timezone}
            onChange={(event) => updateField('timezone', event.target.value)}
          />
        </label>

        {formState.scheduleType === 'once' ? (
          <label className="event-form__field event-form__field--full">
            <span>Run At</span>
            <input
              type="datetime-local"
              name="runAt"
              value={formState.runAt}
              onChange={(event) => updateField('runAt', event.target.value)}
            />
          </label>
        ) : (
          <label className="event-form__field">
            <span>Time Of Day</span>
            <input
              type="time"
              name="timeOfDay"
              value={formState.timeOfDay}
              onChange={(event) => updateField('timeOfDay', event.target.value)}
            />
          </label>
        )}

        {formState.scheduleType === 'weekly' ? (
          <fieldset className="event-form__field event-form__field--full event-form__group">
            <legend>Weekdays</legend>
            <div className="event-form__pill-row">
              {weekdayOptions.map((weekday) => (
                <label key={weekday.value} className="event-form__pill">
                  <input
                    type="checkbox"
                    checked={formState.daysOfWeek.includes(weekday.value)}
                    onChange={() => toggleWeekday(weekday.value)}
                  />
                  <span>{weekday.label}</span>
                </label>
              ))}
            </div>
            {errors.daysOfWeek ? (
              <strong className="event-form__error">{errors.daysOfWeek}</strong>
            ) : null}
          </fieldset>
        ) : null}

        <fieldset className="event-form__field event-form__field--full event-form__group">
          <legend>Allowed Tools</legend>
          <div className="event-form__pill-row">
            {toolOptions.map((tool) => (
              <label key={tool.value} className="event-form__pill">
                <input
                  type="checkbox"
                  checked={formState.allowedTools.includes(tool.value)}
                  onChange={() => toggleAllowedTool(tool.value)}
                />
                <span>{tool.label}</span>
              </label>
            ))}
          </div>
          {errors.allowedTools ? (
            <strong className="event-form__error">{errors.allowedTools}</strong>
          ) : null}
        </fieldset>

        <label className="event-form__field">
          <span>Notify Target</span>
          <select
            name="notifyTarget"
            value={formState.notifyTarget}
            onChange={(event) => updateField('notifyTarget', event.target.value)}
          >
            <option value="dashboard">Dashboard</option>
            <option value="slack">Slack</option>
          </select>
        </label>
      </div>

      <div className="event-form__actions">
        <button type="submit" className="event-form__submit">
          Save Draft
        </button>
      </div>
    </form>
  )
}
