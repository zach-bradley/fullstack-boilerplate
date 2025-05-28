export const mutationBase = (mutationName: string,
  fields: string[],
  args:Record<string, any> = {},
  model: string = "") => {
  const argString = Object.keys(args)
    .map((key) => `${key}: $${key}`)
    .join(", ");

  const mutation = `
    mutation ${mutationName}(${Object.keys(args)
      .map((key) => `$${key}: ${args[key]}`)
      .join(", ")}) {
      ${model ? model + " " : ""}(${argString}) { 
        ${fields.join("\n")}
      }
    }
  `;

  return mutation;
};