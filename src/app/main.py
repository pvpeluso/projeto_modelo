from __future__ import annotations

import random
import sys
from typing import Iterable

import pygame
from OpenGL.GL import (
    GL_COLOR_BUFFER_BIT,
    GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST,
    GL_MODELVIEW,
    GL_POINTS,
    GL_PROJECTION,
    GL_QUADS,
    glBegin,
    glClear,
    glClearColor,
    glColor3f,
    glColor3fv,
    glDisable,
    glEnable,
    glEnd,
    glLoadIdentity,
    glMatrixMode,
    glOrtho,
    glPointSize,
    glPopMatrix,
    glPushMatrix,
    glRotatef,
    glTranslatef,
    glVertex2f,
    glVertex3fv,
    glViewport,
)
from OpenGL.GLU import gluPerspective
from pygame.locals import (
    DOUBLEBUF,
    K_DOWN,
    K_EQUALS,
    K_KP_MINUS,
    K_KP_PLUS,
    K_MINUS,
    K_UP,
    KEYDOWN,
    MOUSEWHEEL,
    OPENGL,
    QUIT,
)


WINDOW_SIZE = (960, 720)
BACKGROUND_COLOR = (0.04, 0.05, 0.08, 1.0)
CAMERA_DISTANCE_DEFAULT = 6.0
CAMERA_DISTANCE_MIN = 3.0
CAMERA_DISTANCE_MAX = 10.0
ZOOM_STEP = 0.35
POINT_COUNT = 2000
POINT_SIZE = 3.0
ROTATION_SPEEDS = {
    "x": 47.0,
    "y": 63.0,
    "z": 31.0,
}


def generate_cube_points(total_points: int) -> tuple[tuple[tuple[float, float, float], tuple[float, float, float]], ...]:
    generator = random.Random(42)
    points: list[tuple[tuple[float, float, float], tuple[float, float, float]]] = []

    for _ in range(total_points):
        x = generator.uniform(-1.0, 1.0)
        y = generator.uniform(-1.0, 1.0)
        z = generator.uniform(-1.0, 1.0)
        color = (
            0.2 + (((x + 1.0) / 2.0) * 0.75),
            0.2 + (((y + 1.0) / 2.0) * 0.75),
            0.2 + (((z + 1.0) / 2.0) * 0.75),
        )
        points.append(((x, y, z), color))

    return tuple(points)


CUBE_POINTS = generate_cube_points(POINT_COUNT)


def setup_scene(window_size: Iterable[int]) -> None:
    width, height = window_size
    safe_height = max(height, 1)

    glViewport(0, 0, width, safe_height)
    glClearColor(*BACKGROUND_COLOR)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / safe_height, 0.1, 50.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


def update_angles(
    angles: dict[str, float],
    rotation_speeds: dict[str, float],
    delta_seconds: float,
) -> None:
    for axis in rotation_speeds:
        angles[axis] = (angles[axis] + rotation_speeds[axis] * delta_seconds) % 360.0


def apply_rotation(angles: dict[str, float]) -> None:
    glRotatef(angles["x"], 1.0, 0.0, 0.0)
    glRotatef(angles["y"], 0.0, 1.0, 0.0)
    glRotatef(angles["z"], 0.0, 0.0, 1.0)


def draw_point_cloud() -> None:
    glPointSize(POINT_SIZE)
    glBegin(GL_POINTS)
    for point, color in CUBE_POINTS:
        glColor3fv(color)
        glVertex3fv(point)
    glEnd()


def draw_bar(
    left: float,
    top: float,
    width: float,
    height: float,
    fill_ratio: float,
    fill_color: tuple[float, float, float],
) -> None:
    fill_width = width * fill_ratio
    glBegin(GL_QUADS)
    glColor3f(0.20, 0.22, 0.28)
    glVertex2f(left, top)
    glVertex2f(left + width, top)
    glVertex2f(left + width, top + height)
    glVertex2f(left, top + height)

    glColor3f(*fill_color)
    glVertex2f(left, top)
    glVertex2f(left + fill_width, top)
    glVertex2f(left + fill_width, top + height)
    glVertex2f(left, top + height)
    glEnd()


def draw_zoom_overlay(window_size: Iterable[int], camera_distance: float) -> None:
    width, height = window_size
    margin = 28.0
    bar_width = 220.0
    bar_height = 16.0
    fill_ratio = (CAMERA_DISTANCE_MAX - camera_distance) / (
        CAMERA_DISTANCE_MAX - CAMERA_DISTANCE_MIN
    )
    left = margin
    top = height - margin - bar_height

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, width, height, 0, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    draw_bar(left, top, bar_width, bar_height, fill_ratio, (0.26, 0.76, 0.98))
    glEnable(GL_DEPTH_TEST)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Nuvem de Pontos 3D")
    pygame.display.set_mode(WINDOW_SIZE, DOUBLEBUF | OPENGL)

    setup_scene(WINDOW_SIZE)

    clock = pygame.time.Clock()
    angles = {"x": 0.0, "y": 0.0, "z": 0.0}
    camera_distance = CAMERA_DISTANCE_DEFAULT

    running = True
    while running:
        delta_seconds = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key in (K_EQUALS, K_KP_PLUS, K_UP):
                    camera_distance = clamp(
                        camera_distance - ZOOM_STEP,
                        CAMERA_DISTANCE_MIN,
                        CAMERA_DISTANCE_MAX,
                    )
                elif event.key in (K_MINUS, K_KP_MINUS, K_DOWN):
                    camera_distance = clamp(
                        camera_distance + ZOOM_STEP,
                        CAMERA_DISTANCE_MIN,
                        CAMERA_DISTANCE_MAX,
                    )
            elif event.type == MOUSEWHEEL:
                camera_distance = clamp(
                    camera_distance - (event.y * ZOOM_STEP),
                    CAMERA_DISTANCE_MIN,
                    CAMERA_DISTANCE_MAX,
                )

        update_angles(angles, ROTATION_SPEEDS, delta_seconds)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -camera_distance)
        apply_rotation(angles)
        draw_point_cloud()
        draw_zoom_overlay(WINDOW_SIZE, camera_distance)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
