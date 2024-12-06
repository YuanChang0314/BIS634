from mpi4py import MPI
import numpy as np
import matplotlib.pyplot as plt
import time

xlo = -2.5
ylo = -1.5
yhi = 1.5
xhi = 0.75
nx = 2048
ny = 1536
dx = (xhi - xlo) / nx
dy = (yhi - ylo) / ny

iter_limit = 200
set_threshold = 2

def mandelbrot_test(x, y):
    z = 0
    c = x + y * 1j
    for i in range(iter_limit):
        z = z ** 2 + c
        if abs(z) > set_threshold:
            return i
    return i

def calculate_set(start_row, end_row):
    result = np.zeros([end_row - start_row, nx])
    for i, row in enumerate(range(start_row, end_row)):
        y = row * dy + ylo
        for j in range(nx):
            x = j * dx + xlo
            result[i, j] = mandelbrot_test(x, y)
    return result

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    rankrow = ny // size
    remainrow = ny % size

    if rank < remainrow:
        currentrow = rank * (rankrow + 1)
        i = rankrow + 1
    else:
        currentrow = rank * rankrow + remainrow
        i = rankrow

    start_time = time.perf_counter()
    local_result = calculate_set(currentrow, i)
    stop_time = time.perf_counter()
    print(f"Rank {rank}: Calculation took {stop_time - start_time} seconds")
    if rank == 0:
        final_result = np.zeros([ny, nx])
    else:
        final_result = None

    counts = np.array([rankrow + 1 if i < remainrow else rankrow for i in range(size)]) * nx
    displacements = np.cumsum(np.insert(counts[:-1], 0, 0))

    comm.Gatherv(sendbuf=local_result,
                 recvbuf=(final_result, counts, displacements, MPI.DOUBLE),
                 root=0)

    if rank == 0:
        plt.imshow(final_result, interpolation="nearest", cmap="Greys")
        plt.gca().set_aspect("equal")
        plt.axis("off")
        plt.show()