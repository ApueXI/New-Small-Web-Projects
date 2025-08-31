import { Link } from "react-router-dom";
import { deleteData } from "../API/issuetracker";
import { useContext } from "react";
import { LoadDataContext } from "../Pages/Home";

export default function IssueCard({ data }) {
  const priorityText = () => {
    if (data.priority_level >= 7) return "High Priority";
    else if (data.priority_level >= 4) return "Medium Priority";
    else return "Low Priority";
  };

  const loadData = useContext(LoadDataContext);

  const handleDelete = () => {
    deleteData(data.id);
    loadData();
  };

  return (
    <div className="bg-color-primary-accent-yellow flex flex-col gap-1 w-full text-[clamp(15px,2vw,20px)] rounded-lg px-5 py-2">
      <h5 className="text-[clamp(18px,2vw,23px)] font-black">
        #{data.id} {data.title}
      </h5>
      <h3>{priorityText()}</h3>
      <div className="inline-block mx-auto space-x-7 cardButton formPointer">
        <Link
          to={`/view/${data.id}`}
          state={{ data }}
          className="hover:scale-125 active:scale-125 transi inline-block"
        >
          View
        </Link>
        <button onClick={handleDelete}>Delete</button>
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
