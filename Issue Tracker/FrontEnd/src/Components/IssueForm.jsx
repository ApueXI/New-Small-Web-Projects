export default function IssueForm({hideForm}) {
  return (
    <div className="relative flex-Col-Center">
      <div className="h-[550px] sm:w-[clamp(200px,60vw,600px)] w-[90%] fixed rounded-md flex-Col-Center bg-[#3F3075] ">
        <button
          onClick={hideForm}
          className="text-[clamp(20px,1.3vw,50px)] px-2 py-1.5 font-bold rounded-lg bg-red-500 ml-auto mr-5 my-3 transi hover:bg-red-700 active:bg-red-700 hover:scale-120 active:scale-120"
        >
          Cancel
        </button>

        <form className="bg-red-500 w-[80%] font-bold p-5 rounded-lg flex flex-col gap-y-2">
          <div className="flex">
            <label htmlFor="title">Title:</label>
            <input type="text" name="title" id="title" className="formInput" />
          </div>

          <div className="flex">
            <label htmlFor="priority">Priority Level: </label>
            <input
              type="number"
              name="priority"
              id="priority"
              className="formInput"
            />
          </div>

          <label htmlFor="issueDetail">Issue Detail:</label>
          <textarea
            name="issueDetail"
            id="issueDetail"
            className="formInput w-[90%] mx-auto"
          ></textarea>
        </form>
      </div>
    </div>
  );
}
