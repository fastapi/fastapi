import * as fs from "fs";

const filePath = "./openapi.json";

fs.readFile(filePath, (err, data) => {
  const openapiContent = JSON.parse(data);
  if (err) throw err;

  const paths = openapiContent.paths;

  Object.keys(paths).forEach((pathKey) => {
    const pathData = paths[pathKey];
    Object.keys(pathData).forEach((method) => {
      const operation = pathData[method];
      if (operation.tags && operation.tags.length > 0) {
        const tag = operation.tags[0];
        const operationId = operation.operationId;
        const toRemove = `${tag}-`;
        if (operationId.startsWith(toRemove)) {
          const newOperationId = operationId.substring(toRemove.length);
          operation.operationId = newOperationId;
        }
      }
    });
  });
  fs.writeFile(filePath, JSON.stringify(openapiContent, null, 2), (err) => {
    if (err) throw err;
  });
});
