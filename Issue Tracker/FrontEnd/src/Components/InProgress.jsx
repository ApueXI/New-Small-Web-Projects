import IssueCard from "./IssueCard";

export default function InProgress() {
  return (
    <div className="bg-blue-600 issueCard flex-Col-Center">
      <h1 className="bg-blue-400 issueTitle">In Progess</h1>
      <div className="issueItem">
        <IssueCard priority={7}></IssueCard>
        <IssueCard priority={2}></IssueCard>
        <IssueCard priority={4}></IssueCard>
        <IssueCard priority={30}></IssueCard>
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
