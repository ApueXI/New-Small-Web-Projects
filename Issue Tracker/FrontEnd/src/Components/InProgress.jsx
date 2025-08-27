import IssueCard from "./IssueCard";

export default function InProgress({ datas }) {
  return (
    <div className="bg-blue-600 issueCard flex-Col-Center">
      <h1 className="bg-blue-400 issueTitle">In Progress</h1>
      <div className="issueItem">
        {datas.map((data) => (
          <IssueCard
            key={data.id}
            data={data}
          />
        ))}
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
