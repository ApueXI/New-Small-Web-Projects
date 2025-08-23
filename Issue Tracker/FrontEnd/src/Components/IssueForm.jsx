export default function IssueForm({ hideForm }) {
  const submitData = (e) => {
    e.preventDefault();
    console.log("Submiteted Data");
    hideForm();
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
          onSubmit={submitData}
          className="bg-[hsl(253,42%,72%)] text-[clamp(15px,2vw,25px)]  w-[80%] font-bold p-5 rounded-lg flex flex-col gap-y-5 formPointer"
        >
          <div className="flex flex-col">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              name="title"
              id="title"
              placeholder="e.g. #10 Log-in Form Bug"
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
              className="formInput"
            />
          </div>

          <div className="flex flex-col">
            <label htmlFor="issueDetail">Issue Detail:</label>
            <textarea
              name="issueDetail"
              id="issueDetail"
              placeholder="Log-in form returns an error whenever i submit it"
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
