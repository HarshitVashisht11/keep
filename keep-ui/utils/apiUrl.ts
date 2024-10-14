export function getApiURL(): string {
  const componentType = typeof window === "undefined" ? "server" : "client";

  if (componentType === "client") {
    return "/backend";
  }

  // SERVER ONLY FROM HERE ON
  const gitBranchName = process.env.VERCEL_GIT_COMMIT_REF || "notvercel";

  if (gitBranchName === "main" || gitBranchName === "notvercel") {
    return process.env.API_URL!;
  } else {
    console.log("preview branch on vercel");
    let branchNameSanitized = gitBranchName.replace(/\//g, "-");
    const maxBranchNameLength = 40; // 63 - "keep-api-".length - "-3jg67kxyna-uc".length;
    if (branchNameSanitized.length > maxBranchNameLength) {
      branchNameSanitized = branchNameSanitized.substring(
        0,
        maxBranchNameLength
      );
    }
    let serviceName = `keep-api-${branchNameSanitized}`;
    return process.env.API_URL!.replace("keep-api", serviceName);
  }
}
