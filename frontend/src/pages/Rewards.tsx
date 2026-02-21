import type { UserProfile } from "../types";

interface Reward {
    id: string;
    name: string;
    price: number;
    image: string;
    description: string;
}

const REWARDS_LIST: Reward[] = [
    {
        id: "r1",
        name: "Bamboo Toothbrush Set",
        price: 500,
        description: "4-pack of eco-friendly, biodegradable bamboo toothbrushes.",
        image: "https://images.unsplash.com/photo-1607613009820-a29f7bb81c04?auto=format&fit=crop&w=800&q=80",
    },
    {
        id: "r2",
        name: "Organic Composting Bin",
        price: 1200,
        description: "Compact indoor composter for your kitchen scraps.",
        image: "https://images.unsplash.com/photo-1591857177580-dc82b9ac4e1e?auto=format&fit=crop&w=800&q=80",
    },
    {
        id: "r3",
        name: "Native Tree Sapling",
        price: 300,
        description: "We'll plant a native tree in your name or ship one to you.",
        image: "https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?auto=format&fit=crop&w=800&q=80",
    },
    {
        id: "r4",
        name: "Reusable Produce Bags",
        price: 250,
        description: "Set of 5 cotton mesh bags for plastic-free grocery shopping.",
        image: "https://images.unsplash.com/photo-1610557892470-55d9e80c0bce?auto=format&fit=crop&w=800&q=80",
    },
];

export default function Rewards({ profile }: { profile: UserProfile | null }) {
    const points = profile?.total_points ?? 0;

    return (
        <div className="mx-auto max-w-lg">
            <header className="sticky top-0 z-40 bg-white/80 px-4 py-6 backdrop-blur-md">
                <div className="flex items-center justify-between">
                    <h1 className="text-xl font-bold text-terra-900">Rewards</h1>
                    <div className="flex items-center gap-2 rounded-full bg-earth-500 px-4 py-1.5 text-white shadow-lg shadow-earth-200">
                        <span className="text-lg">🌟</span>
                        <span className="font-bold">{points.toLocaleString()}</span>
                    </div>
                </div>
                <p className="mt-1 text-xs font-semibold uppercase tracking-widest text-gray-400">
                    Redeem your impact points
                </p>
            </header>

            <div className="grid grid-cols-2 gap-4 p-4">
                {REWARDS_LIST.map((reward) => (
                    <div
                        key={reward.id}
                        className="flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-gray-100"
                    >
                        <div className="relative aspect-square">
                            <img
                                src={reward.image}
                                alt={reward.name}
                                className="h-full w-full object-cover"
                            />
                            <div className="absolute bottom-2 right-2 rounded-lg bg-black/60 px-2 py-1 text-xs font-bold text-white backdrop-blur-sm">
                                {reward.price} pts
                            </div>
                        </div>
                        <div className="flex flex-1 flex-col p-3">
                            <h3 className="text-sm font-bold text-terra-900 line-clamp-1">{reward.name}</h3>
                            <p className="mt-1 text-[11px] leading-tight text-gray-500 line-clamp-2">
                                {reward.description}
                            </p>
                            <button
                                disabled={points < reward.price}
                                className={`mt-3 w-full rounded-lg py-2 text-xs font-bold transition ${points >= reward.price
                                        ? "bg-terra-600 text-white hover:bg-terra-700"
                                        : "bg-gray-100 text-gray-400 cursor-not-allowed"
                                    }`}
                            >
                                {points >= reward.price ? "Redeem" : "Insufficient Pts"}
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            <div className="mt-8 px-4 pb-12">
                <div className="rounded-2xl bg-gradient-to-br from-terra-700 to-terra-800 p-6 text-white shadow-xl">
                    <h2 className="text-lg font-bold">Earn more points?</h2>
                    <p className="mt-2 text-sm text-terra-100 opacity-90">
                        Complete eco-actions, participate in community challenges, and invite friends to level up your impact.
                    </p>
                    <button className="mt-6 w-full rounded-xl bg-white py-3 text-sm font-bold text-terra-800 transition hover:bg-terra-50">
                        View Challenges
                    </button>
                </div>
            </div>
        </div>
    );
}
