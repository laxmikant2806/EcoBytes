/**
 * Firebase SDK initialization — single entry point.
 * Firestore (db) and Storage are kept for data/file storage.
 * Firebase Auth has been removed — authentication is now handled
 * by a custom JWT system (see services/auth.ts).
 *
 * All other files import db and storage from here.
 * Never import directly from "firebase/firestore", "firebase/storage", etc.
 */

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";
import { getStorage } from "firebase/storage";
import { config } from "./config";

const app = initializeApp(config.firebase);

export const db      = getFirestore(app);
export const storage = getStorage(app);
