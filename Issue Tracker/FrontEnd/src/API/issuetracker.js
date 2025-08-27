const ITPrefix = "/api";
const ITGet = "/issue/get";
const ITSend = "/issue/send";

export const getData = async (sort = "asc") => {
  try {
    const response = await fetch(`${ITPrefix}${ITGet}?sort=${sort}`);
    const data = await response.json();

    console.log("----------------------------");
    console.log({ response, data });
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const sendData = async (dataToSend) => {
  try {
    const response = await fetch(`${ITPrefix}${ITSend}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToSend),
    });
    const data = await response.json();

    console.log("----------------------------");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};
