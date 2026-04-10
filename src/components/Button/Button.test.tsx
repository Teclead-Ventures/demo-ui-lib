import { render, screen } from "@testing-library/react";
import { Button } from "./Button";

describe("Button", () => {
  it("renders children", () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole("button", { name: "Click me" })).toBeInTheDocument();
  });

  it("applies variant", () => {
    render(<Button variant="secondary">Click me</Button>);
    expect(screen.getByRole("button")).toHaveAttribute("data-variant", "secondary");
  });
});
