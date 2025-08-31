const ITPrefix = "/api";
const ITGet = "/issue/get";
const ITSend = "/issue/send";
const ITDelete = "/issue/delete";
const ITUpdate = "/issue/update";

export const getData = async (query, sort = "desc") => {
  try {
    const response = await fetch(
      `${ITPrefix}${ITGet}?sort=${sort}&query=${query}`
    );

    const data = await response.json();

    console.log("----------------------------");
    console.log(`From GetData ${query}`);
    console.log({ response, data });
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const getIndividualData = async (id) => {
  try {
    const response = await fetch(`${ITPrefix}${ITGet}/${id}`);

    const data = await response.json();

    console.log("----------------------------");
    console.log("From GetIndividualData");
    console.log({ response, data });
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error" ${error}`);
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
    console.log("From SendData");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const deleteData = async (id) => {
  try {
    const response = await fetch(`${ITPrefix}${ITDelete}/${id}`, {
      method: "DELETE",
    });

    const data = await response.json();

    console.log("----------------------------");
    console.log("From DeleteData");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};

export const updateData = async (id, dataToUpdate) => {
  try {
    const response = await fetch(`${ITPrefix}${ITDelete}/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(dataToUpdate),
    });

    const data = await response.json();

    console.log("----------------------------");
    console.log("From UpdateData");
    console.log({ response, data });
    console.log(`Sent to the backend: ${data.status}`);
    console.log("----------------------------");

    return data;
  } catch (error) {
    throw new Error(`Error: ${error}`);
  }
};
