import IssueCard from "./IssueCard";

export default function Open() {
  return (
    <div className="bg-red-500 issueCard flex-Col-Center">
      <h1 className="bg-red-300 issueTitle">OPEN</h1>
      <div className="issueItem">
        <IssueCard priority={7}></IssueCard>
        <IssueCard priority={2}></IssueCard>
        <IssueCard priority={4}></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
        <IssueCard></IssueCard>
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
