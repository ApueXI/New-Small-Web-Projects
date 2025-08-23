export default function IssueCard({ title = "No Title", priority = 50 }) {
  const priorityText = () => {
    if (priority >= 7) {
      return "High Priority";
    } else if (priority >= 4) {
      return "Medium Priority";
    } else {
      return "Low Priority";
    }
  };

  return (
    <div className="bg-color-primary-accent-yellow flex flex-col gap-1 w-full text-[clamp(15px,1.5vw,25px)] rounded-lg px-5 py-2">
      <h5>Title: {title}</h5>
      <h5>Priority: {priorityText()}</h5>
      <div className="inline-block mx-auto space-x-7 cardButton">
        <button>View</button>
        <button>Edit</button>
      </div>
    </div>
  );
}

// ┌─────────────────────────────────────────────┐
// │                 🐞 Issue Tracker             │
// │─────────────────────────────────────────────│
// │ [ + New Issue ]                              │
// │                                             │
// │ ┌────── Open ──────┐  ┌── In Progress ─┐  ┌── Resolved ──┐
// │ │ #45  Login fails │  │ #39  CSS bugs  │  │ #21  Fixed   │
// │ │ High priority    │  │ Medium prio.   │  │ Login fixed  │
// │ │ [View] [Edit]    │  │ [View] [Edit]  │  │ [View]       │
// │ └──────────────────┘  └────────────────┘  └──────────────┘
// │                                             │
// └─────────────────────────────────────────────┘
