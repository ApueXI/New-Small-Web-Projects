export default function Home() {
  return (
    <div className="space-y-5">
      <h1 className="text-4xl text-red-500">Hellowoworld</h1>
      <h1 className="text-4xl text-green-500">Hellowoworld</h1>
      <h1 className="text-4xl text-blue-500">Hellowoworld</h1>
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