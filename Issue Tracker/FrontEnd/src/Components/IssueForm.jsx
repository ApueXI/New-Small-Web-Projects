import { useState } from "react";

export default function IssueForm({ hideForm, data, submitData }) {
  const [titleData, setTitleData] = useState(data?.title || null);
  const [priorityLevelData, setPriorityLevelData] = useState(
    data?.priority_level || null
  );
  const [detailsData, setDetailsData] = useState(data?.details || null);

  const handleSubmit = (e) => {
    e.preventDefault();

    const submitDatas = {};

    submitDatas.title = titleData.trim();
    submitDatas.priority_level = priorityLevelData;
    submitDatas.details = detailsData.trim();

    submitData(submitDatas);

    if (!data) {
      setTitleData("");
      setPriorityLevelData(1);
      setDetailsData("");
    }

    console.log("Submitted to the backend");
  };

  return (
    <div className="relative flex-Col-Center">
      <div className="sm:w-[clamp(200px,60vw,600px)] w-[90%] pb-13 fixed rounded-md flex-Col-Center bg-[#3F3075] ">
        <div className="flex w-full">
          <h1 className="my-auto ml-6 bg-[hsl(253,42%,62%)] font-bold px-2 py-1.5 rounded-lg text-[clamp(20px,1.3vw,50px)]">
            Add a new Issue
          </h1>
          <button
            onClick={hideForm}
            className="text-[clamp(20px,1.3vw,50px)] px-2 py-1.5 font-bold rounded-lg ml-auto mr-5 my-5 transi cursor-pointer bg-red-500 hover:bg-red-700 active:bg-red-700 hover:scale-120 active:scale-120"
          >
            Cancel
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="bg-[hsl(253,42%,72%)] text-[clamp(15px,2vw,25px)]  w-[80%] font-bold p-5 rounded-lg flex flex-col gap-y-5 formPointer"
        >
          <div className="flex flex-col">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              name="title"
              id="title"
              placeholder="e.g. Log-in Form Bug"
              value={titleData}
              onChange={(e) => setTitleData(e.target.value)}
              className="formInput"
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="priority">Priority Level: </label>
            <input
              type="number"
              name="priority"
              id="priority"
              placeholder="1-10"
              min={1}
              max={10}
              value={priorityLevelData}
              onChange={(e) => setPriorityLevelData(Number(e.target.value))}
              className="formInput"
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="issueDetail">Issue Detail:</label>
            <textarea
              name="issueDetail"
              id="issueDetail"
              placeholder="e.g. Log-in form returns an error whenever i submit it"
              value={detailsData}
              onChange={(e) => setDetailsData(e.target.value)}
              className="formInput"
            ></textarea>
          </div>

          <input
            type="submit"
            name="submit"
            id="submit"
            className="mx-auto px-2 py-1.5 rounded-lg transi bg-[hsl(253,42%,22%)] text-white hover:bg-[hsl(253,42%,42%)] active:bg-[hsl(253,42%,42%)] hover:scale-120 active:scale-120"
          />
        </form>
      </div>
    </div>
  );
}
