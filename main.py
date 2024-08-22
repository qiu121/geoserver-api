from tasks.workspace import create_workspace
from tasks.coveragestore import create_coverage_store
from tasks.layer import create_layer

if __name__ == '__main__':
    # 顺序执行所有步骤
    if create_workspace() == 201:  # Workspace 创建成功
        if create_coverage_store() == 201:  # CoverageStore 创建成功
            create_layer()  # 尝试创建 layer

