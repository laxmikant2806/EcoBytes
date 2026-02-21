import { Outlet } from "react-router-dom";
import Navigation from "./Navigation";

export default function Layout() {
    return (
        <div className="flex min-h-screen flex-col bg-terra-50 pb-20">
            <main className="flex-1">
                <Outlet />
            </main>
            <Navigation />
        </div>
    );
}
