"""
性能测试脚本
Performance Testing Script

测试项目的性能指标和优化效果
"""

import time
import sys
import gc
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import requests

try:
    from performance_config import get_all_performance_config, PERFORMANCE_TIPS
    from http_client import HttpClient
    from logging_config import get_logger
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保在项目根目录运行此脚本")
    sys.exit(1)

log = get_logger()


class PerformanceTester:
    """性能测试器"""
    
    def __init__(self):
        self.results = []
        self.config = get_all_performance_config()
    
    def test_http_performance(self, url: str = "https://httpbin.org/get", count: int = 100):
        """
        测试HTTP性能
        
        Args:
            url: 测试URL
            count: 请求次数
        """
        print(f"\n{'='*60}")
        print("🚀 HTTP性能测试")
        print(f"{'='*60}")
        print(f"测试URL: {url}")
        print(f"请求次数: {count}")
        
        client = HttpClient()
        
        # 串行测试
        print("\n📊 串行请求测试...")
        start_time = time.time()
        success_count = 0
        
        for i in range(count):
            try:
                response = client.get(url)
                if response.status_code == 200:
                    success_count += 1
            except Exception as e:
                log.error(f"请求失败: {e}")
        
        serial_time = time.time() - start_time
        serial_rps = count / serial_time if serial_time > 0 else 0
        
        print(f"✅ 完成: {success_count}/{count}")
        print(f"⏱️  耗时: {serial_time:.2f}秒")
        print(f"🔥 RPS: {serial_rps:.2f} 请求/秒")
        
        # 并发测试
        print("\n📊 并发请求测试（优化后）...")
        max_workers = self.config['concurrent']['max_workers']
        print(f"线程数: {max_workers}")
        
        start_time = time.time()
        success_count = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(client.get, url) for _ in range(count)]
            
            for future in as_completed(futures):
                try:
                    response = future.result()
                    if response.status_code == 200:
                        success_count += 1
                except Exception as e:
                    log.error(f"并发请求失败: {e}")
        
        concurrent_time = time.time() - start_time
        concurrent_rps = count / concurrent_time if concurrent_time > 0 else 0
        
        print(f"✅ 完成: {success_count}/{count}")
        print(f"⏱️  耗时: {concurrent_time:.2f}秒")
        print(f"🔥 RPS: {concurrent_rps:.2f} 请求/秒")
        
        # 性能提升
        speedup = serial_time / concurrent_time if concurrent_time > 0 else 0
        improvement = ((serial_time - concurrent_time) / serial_time * 100) if serial_time > 0 else 0
        
        print(f"\n{'='*60}")
        print("📈 性能对比")
        print(f"{'='*60}")
        print(f"加速比: {speedup:.2f}x")
        print(f"性能提升: {improvement:.1f}%")
        
        return {
            'serial': {'time': serial_time, 'rps': serial_rps},
            'concurrent': {'time': concurrent_time, 'rps': concurrent_rps},
            'speedup': speedup,
            'improvement': improvement
        }
    
    def test_memory_usage(self):
        """测试内存使用"""
        print(f"\n{'='*60}")
        print("💾 内存使用测试")
        print(f"{'='*60}")
        
        try:
            import psutil
            process = psutil.Process()
            
            # 运行GC
            gc.collect()
            
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            print(f"GC前内存: {mem_before:.2f} MB")
            
            # 创建一些对象
            data = [i for i in range(1000000)]
            mem_during = process.memory_info().rss / 1024 / 1024  # MB
            print(f"创建对象后: {mem_during:.2f} MB (+{mem_during - mem_before:.2f} MB)")
            
            # 清理
            del data
            gc.collect()
            
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            print(f"GC后内存: {mem_after:.2f} MB (回收 {mem_during - mem_after:.2f} MB)")
            
            return {
                'before': mem_before,
                'peak': mem_during,
                'after': mem_after,
                'recovered': mem_during - mem_after
            }
        except ImportError:
            print("⚠️  psutil未安装，跳过内存测试")
            print("提示: pip install psutil")
            return None
    
    def test_import_speed(self):
        """测试模块导入速度"""
        print(f"\n{'='*60}")
        print("📦 模块导入速度测试")
        print(f"{'='*60}")
        
        modules = ['requests', 'pytest', 'PyYAML', 'jsonpath_ng', 'colorama']
        results = {}
        
        for module_name in modules:
            try:
                start_time = time.time()
                __import__(module_name)
                import_time = (time.time() - start_time) * 1000  # 毫秒
                results[module_name] = import_time
                print(f"✅ {module_name}: {import_time:.2f}ms")
            except ImportError:
                print(f"⚠️  {module_name}: 未安装")
                results[module_name] = None
        
        return results
    
    def test_response_time(self, url: str = "https://httpbin.org/delay/1"):
        """测试响应时间"""
        print(f"\n{'='*60}")
        print("⏱️  响应时间测试")
        print(f"{'='*60}")
        
        client = HttpClient()
        times = []
        
        for i in range(10):
            try:
                start = time.time()
                response = client.get(url)
                elapsed = (time.time() - start) * 1000  # 毫秒
                times.append(elapsed)
                print(f"请求 {i+1}: {elapsed:.2f}ms")
            except Exception as e:
                print(f"请求 {i+1}: 失败 - {e}")
        
        if times:
            avg_time = sum(times) / len(times)
            min_time = min(times)
            max_time = max(times)
            
            print(f"\n统计:")
            print(f"平均: {avg_time:.2f}ms")
            print(f"最小: {min_time:.2f}ms")
            print(f"最大: {max_time:.2f}ms")
            
            return {
                'avg': avg_time,
                'min': min_time,
                'max': max_time,
                'times': times
            }
        
        return None
    
    def run_all_tests(self):
        """运行所有性能测试"""
        print("\n" + "🎯 " + "="*58)
        print("    YH API 性能测试套件")
        print("="*60)
        
        results = {}
        
        # 1. 导入速度测试
        results['import'] = self.test_import_speed()
        
        # 2. HTTP性能测试
        try:
            results['http'] = self.test_http_performance(count=50)
        except Exception as e:
            print(f"❌ HTTP测试失败: {e}")
            results['http'] = None
        
        # 3. 响应时间测试（跳过延迟测试以加快速度）
        # results['response'] = self.test_response_time()
        
        # 4. 内存测试
        results['memory'] = self.test_memory_usage()
        
        # 生成报告
        self._generate_report(results)
        
        return results
    
    def _generate_report(self, results: Dict[str, Any]):
        """生成性能报告"""
        print(f"\n{'='*60}")
        print("📊 性能测试报告")
        print(f"{'='*60}\n")
        
        # HTTP性能
        if results.get('http'):
            http = results['http']
            print(f"🚀 HTTP性能:")
            print(f"   并发RPS: {http['concurrent']['rps']:.2f} 请求/秒")
            print(f"   性能提升: {http['improvement']:.1f}%")
            print(f"   加速比: {http['speedup']:.2f}x\n")
        
        # 内存使用
        if results.get('memory'):
            mem = results['memory']
            print(f"💾 内存管理:")
            print(f"   峰值内存: {mem['peak']:.2f} MB")
            print(f"   GC回收: {mem['recovered']:.2f} MB\n")
        
        # 建议
        print(f"💡 优化建议:")
        print(PERFORMANCE_TIPS)


def main():
    """主函数"""
    tester = PerformanceTester()
    
    # 运行所有测试
    results = tester.run_all_tests()
    
    print(f"\n{'='*60}")
    print("✅ 测试完成！")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
