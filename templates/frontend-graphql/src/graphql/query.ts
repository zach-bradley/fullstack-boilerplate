export const queryBase = (
  queryName: string,
  model: string,
  fields: string[],
  args: Record<string, { type: string; value: any }> = {}
) => {
  // Define the variable declarations in GraphQL format
  const argDefinitions = Object.keys(args)
    .map((key) => `$${key}: ${args[key].type}`)
    .join(", ");

  // Define the arguments for the query (using variable names)
  const argValues = Object.keys(args)
    .map((key) => `${key}: $${key}`)
    .join(", ");

  const query = `
    query ${queryName}(${argDefinitions}) {
      ${model}(${argValues}) { 
        ${fields.join("\n")}
      }
    }
  `;

  return query;
};