export default function TopBar({title = "No Title"}) {

  return (
    <div className="bg-color-muted-gray-yellow flex">
      <h1 className="bg-color-primary-accent-yellow sm:font-bold font-black px-5 py-2 text-[clamp(25px,3vw,50px)] mx-auto my-5 rounded-lg ">{title}</h1>
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
